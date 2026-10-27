"""
Tests for `export_pages_from_sisu`: paging driven by `greatestOrdinal`/`hasMore`, caller-set page
size, and scrambling that rebuilds the yielded page from the scrambler return values.
"""
import httpx
import pytest
from pydantic import BaseModel

from funidata_utils.request_utils import httpx_requests
from funidata_utils.sis_integration import export_pages_from_sisu, ExportPage, export_from_sisu
from funidata_utils.sis_integration.resources import Attainments, CodeBooks


class ExportSettings(BaseModel):
    host: str = 'http://localhost:18080'
    proxies: dict | None = None

    def get_export_auth(self) -> tuple[str, str]:
        return 'lab.e', 'test123'


def _attainment(ordinal: int) -> dict:
    return {
        "id": f"otm-{ordinal}",
        "documentState": "ACTIVE",
        "personId": f"person-{ordinal}",
        "state": "ATTAINED",
        "primaryStatus": "PRIMARY",
        "administrativeNote": "secret note",
        "metadata": {
            "createdBy": "real.user",
            "lastModifiedBy": "real.user",
            "revision": 1,
        },
        "someFutureKey": "value",
    }


class PagedSisu:
    """
    Serves `total` entities with ordinals 1..total. A page is full unless it is the last one.
    `has_more_on_last_full_page` controls the hasMore=false-on-a-full-page case.
    """

    def __init__(self, total: int, has_more_field: bool = True):
        self.total = total
        self.has_more_field = has_more_field
        self.requests: list[dict] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        since = int(request.url.params["since"])
        limit = int(request.url.params["limit"])
        self.requests.append({"since": since, "limit": limit})
        ordinals = [o for o in range(since + 1, self.total + 1)][:limit]
        body = {
            "entities": [_attainment(o) for o in ordinals],
            "greatestOrdinal": ordinals[-1] if ordinals else since,
        }
        if self.has_more_field:
            body["hasMore"] = bool(ordinals) and ordinals[-1] < self.total
        return httpx.Response(200, json=body)

    def install(self, monkeypatch):
        monkeypatch.setattr(
            httpx_requests,
            "_get_httpx_client",
            lambda *args, **kwargs: httpx.Client(transport=httpx.MockTransport(self.handler)),
        )


@pytest.mark.unit
def test_pages_expose_ordinal_and_has_more(monkeypatch):
    sisu = PagedSisu(total=7)
    sisu.install(monkeypatch)

    pages = list(export_pages_from_sisu(ExportSettings(), Attainments, export_limit=3))

    assert [type(p) for p in pages] == [ExportPage] * 3
    assert [len(p.entities) for p in pages] == [3, 3, 1]
    assert [p.greatest_ordinal for p in pages] == [3, 6, 7]
    assert [p.has_more for p in pages] == [True, True, False]
    assert [r["since"] for r in sisu.requests] == [0, 3, 6]
    assert all(r["limit"] == 3 for r in sisu.requests)


@pytest.mark.unit
def test_has_more_false_on_a_full_page_stops_the_export(monkeypatch):
    sisu = PagedSisu(total=6)
    sisu.install(monkeypatch)

    pages = list(export_pages_from_sisu(ExportSettings(), Attainments, export_limit=3))

    assert [len(p.entities) for p in pages] == [3, 3]
    assert pages[-1].has_more is False
    assert len(sisu.requests) == 2


@pytest.mark.unit
def test_falls_back_to_page_size_when_has_more_is_missing(monkeypatch):
    sisu = PagedSisu(total=6, has_more_field=False)
    sisu.install(monkeypatch)

    pages = list(export_pages_from_sisu(ExportSettings(), Attainments, export_limit=3))

    # Two full pages, then one empty page tells the export to stop.
    assert [len(p.entities) for p in pages] == [3, 3, 0]
    assert [p.has_more for p in pages] == [True, True, False]
    assert pages[-1].greatest_ordinal == 6


@pytest.mark.unit
def test_since_ordinal_and_default_limit(monkeypatch):
    sisu = PagedSisu(total=5)
    sisu.install(monkeypatch)

    pages = list(export_pages_from_sisu(ExportSettings(), Attainments, since_ordinal=4))

    assert [r["since"] for r in sisu.requests] == [4]
    assert sisu.requests[0]["limit"] == Attainments.exports.default_export_limit
    assert [e["id"] for e in pages[0].entities] == ["otm-5"]


@pytest.mark.unit
def test_scrambled_pages_use_scrambler_output(monkeypatch, caplog):
    sisu = PagedSisu(total=2)
    sisu.install(monkeypatch)

    with caplog.at_level("WARNING", logger="funidata_utils.sis_integration.exports"):
        pages = list(export_pages_from_sisu(ExportSettings(), Attainments, scramble=True))

    entity = pages[0].entities[0]
    assert entity["personId"] == "person-1"
    assert entity["primaryStatus"] == "PRIMARY"
    assert entity["administrativeNote"] == "administrativeNote"
    assert entity["metadata"]["createdBy"] == "Lorem"
    assert "someFutureKey" not in entity
    assert "someFutureKey" in caplog.text


@pytest.mark.unit
def test_unscrambled_pages_are_untouched(monkeypatch):
    sisu = PagedSisu(total=1)
    sisu.install(monkeypatch)

    pages = list(export_pages_from_sisu(ExportSettings(), Attainments))

    assert pages[0].entities == [_attainment(1)]


@pytest.mark.unit
def test_scramble_requires_scrambling_classes(monkeypatch):
    sisu = PagedSisu(total=1)
    sisu.install(monkeypatch)

    with pytest.raises(AttributeError):
        export_pages_from_sisu(ExportSettings(), CodeBooks, scramble=True)


@pytest.mark.unit
def test_non_200_raises(monkeypatch):
    monkeypatch.setattr(
        httpx_requests,
        "_get_httpx_client",
        lambda *args, **kwargs: httpx.Client(
            transport=httpx.MockTransport(lambda request: httpx.Response(503, text="down"))
        ),
    )

    with pytest.raises(Exception, match="503"):
        next(export_pages_from_sisu(ExportSettings(), Attainments))


@pytest.mark.unit
def test_export_from_sisu_still_collects_all_pages(monkeypatch):
    sisu = PagedSisu(total=7)
    sisu.install(monkeypatch)

    entities = export_from_sisu(ExportSettings(), Attainments)

    assert [e["id"] for e in entities] == [f"otm-{o}" for o in range(1, 8)]
