"""
Tests for the async exports in `funidata_utils.sis_integration.async_exports`, plus the
`iterate_async_generator` helper that the sync wrappers are built on.
"""
import io
import json

import httpx
import pytest

from funidata_utils.request_utils import async_httpx_requests
from funidata_utils.sis_integration import async_export_pages_from_sisu, async_export_from_sisu, ExportPage
from funidata_utils.sis_integration.async_exports import export_pages_from_sisu, export_from_sisu
from funidata_utils.sis_integration.resources import Attainments, CodeBooks
from funidata_utils.utils import iterate_async_generator
from tests.test_export_pages import ExportSettings, PagedSisu, ShortPagedSisu, StuckSisu, _attainment


def test_package_exposes_async_functions_under_prefixed_names():
    assert async_export_pages_from_sisu is export_pages_from_sisu
    assert async_export_from_sisu is export_from_sisu


@pytest.mark.unit
@pytest.mark.asyncio
async def test_pages_expose_ordinal_and_has_more(monkeypatch):
    sisu = PagedSisu(total=7)
    sisu.install(monkeypatch)

    pages = [p async for p in export_pages_from_sisu(ExportSettings(), Attainments, export_limit=3)]

    assert [type(p) for p in pages] == [ExportPage] * 3
    assert [len(p.entities) for p in pages] == [3, 3, 1]
    assert [p.greatest_ordinal for p in pages] == [3, 6, 7]
    assert [p.has_more for p in pages] == [True, True, False]
    assert [r["since"] for r in sisu.requests] == [0, 3, 6]
    assert all(r["limit"] == 3 for r in sisu.requests)


@pytest.mark.unit
@pytest.mark.asyncio
@pytest.mark.parametrize("report_ordinal", [True, False])
async def test_non_advancing_ordinal_raises_instead_of_looping(monkeypatch, report_ordinal):
    sisu = StuckSisu(report_ordinal=report_ordinal)
    sisu.install(monkeypatch)

    with pytest.raises(Exception, match="greatestOrdinal did not advance"):
        [p async for p in export_pages_from_sisu(ExportSettings(), Attainments, since_ordinal=4)]

    assert [r["since"] for r in sisu.requests] == [4]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_falls_back_to_page_size_when_has_more_is_missing(monkeypatch):
    sisu = PagedSisu(total=6, has_more_field=False)
    sisu.install(monkeypatch)

    pages = [p async for p in export_pages_from_sisu(ExportSettings(), Attainments, export_limit=3)]

    assert [len(p.entities) for p in pages] == [3, 3, 0]
    assert [p.has_more for p in pages] == [True, True, False]
    assert pages[-1].greatest_ordinal == 6


@pytest.mark.unit
@pytest.mark.asyncio
async def test_since_ordinal_and_default_limit(monkeypatch):
    sisu = PagedSisu(total=5)
    sisu.install(monkeypatch)

    pages = [p async for p in export_pages_from_sisu(ExportSettings(), Attainments, since_ordinal=4)]

    assert [r["since"] for r in sisu.requests] == [4]
    assert sisu.requests[0]["limit"] == Attainments.exports.default_export_limit
    assert [e["id"] for e in pages[0].entities] == ["otm-5"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_scrambled_pages_use_scrambler_output(monkeypatch, caplog):
    sisu = PagedSisu(total=2)
    sisu.install(monkeypatch)

    with caplog.at_level("WARNING", logger="funidata_utils.sis_integration.async_exports"):
        pages = [p async for p in export_pages_from_sisu(ExportSettings(), Attainments, scramble=True)]

    entity = pages[0].entities[0]
    assert entity["personId"] == "person-1"
    assert entity["administrativeNote"] == "administrativeNote"
    assert entity["metadata"]["createdBy"] == "Lorem"
    assert "someFutureKey" not in entity
    assert "someFutureKey" in caplog.text


@pytest.mark.unit
def test_scramble_requires_scrambling_classes():
    with pytest.raises(AttributeError):
        export_pages_from_sisu(ExportSettings(), CodeBooks, scramble=True)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_non_200_raises(monkeypatch):
    monkeypatch.setattr(
        async_httpx_requests,
        "_get_async_httpx_client",
        lambda *args, **kwargs: httpx.AsyncClient(
            transport=httpx.MockTransport(lambda request: httpx.Response(503, text="down"))
        ),
    )

    with pytest.raises(Exception, match="503"):
        await anext(export_pages_from_sisu(ExportSettings(), Attainments))


@pytest.mark.unit
@pytest.mark.asyncio
async def test_export_from_sisu_collects_all_pages(monkeypatch):
    sisu = PagedSisu(total=7)
    sisu.install(monkeypatch)

    entities = await export_from_sisu(ExportSettings(), Attainments)

    assert [e["id"] for e in entities] == [f"otm-{o}" for o in range(1, 8)]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_export_from_sisu_follows_has_more_on_short_pages(monkeypatch):
    sisu = ShortPagedSisu(total=7, page_size=2)
    sisu.install(monkeypatch)
    fp = io.StringIO()

    entities = await export_from_sisu(ExportSettings(), Attainments)
    await export_from_sisu(ExportSettings(), Attainments, fp=fp)

    expected = [f"otm-{o}" for o in range(1, 8)]
    assert [e["id"] for e in entities] == expected
    assert [json.loads(line)["id"] for line in fp.getvalue().splitlines()] == expected


@pytest.mark.unit
@pytest.mark.asyncio
async def test_export_from_sisu_writes_jsonl_to_fp(monkeypatch):
    sisu = PagedSisu(total=3)
    sisu.install(monkeypatch)
    fp = io.StringIO()

    returned = await export_from_sisu(ExportSettings(), Attainments, fp=fp)

    assert returned is fp
    lines = fp.getvalue().splitlines()
    assert [json.loads(line) for line in lines] == [_attainment(o) for o in (1, 2, 3)]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_export_from_sisu_as_generator_is_awaited_then_iterated(monkeypatch):
    """Matches how oopsis consumes it: `gen = await export_from_sisu(..., as_generator=True)`."""
    sisu = PagedSisu(total=5)
    sisu.install(monkeypatch)

    gen = await export_from_sisu(ExportSettings(), Attainments, as_generator=True)
    batches = [batch async for batch in gen]

    assert len(batches) == 1
    assert [e["id"] for e in batches[0]] == [f"otm-{o}" for o in range(1, 6)]


@pytest.mark.unit
def test_iterate_async_generator_yields_all_items_and_closes():
    closed = False

    async def agen():
        nonlocal closed
        try:
            for i in range(3):
                yield i
        finally:
            closed = True

    assert list(iterate_async_generator(agen())) == [0, 1, 2]
    assert closed


@pytest.mark.unit
def test_iterate_async_generator_closes_on_early_break():
    closed = False

    async def agen():
        nonlocal closed
        try:
            for i in range(100):
                yield i
        finally:
            closed = True

    sync_gen = iterate_async_generator(agen())
    assert next(sync_gen) == 0
    sync_gen.close()
    assert closed


@pytest.mark.unit
@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore:coroutine 'export_from_sisu' was never awaited:RuntimeWarning")
async def test_sync_wrapper_refuses_to_run_inside_event_loop(monkeypatch):
    from funidata_utils.sis_integration import export_from_sisu as sync_export_from_sisu

    sisu = PagedSisu(total=1)
    sisu.install(monkeypatch)

    with pytest.raises(RuntimeError):
        sync_export_from_sisu(ExportSettings(), Attainments)
