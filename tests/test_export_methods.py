import pytest
from pydantic import BaseModel

from funidata_utils.request_utils import httpx_requests
from funidata_utils.sis_integration.exports import export_from_sisu
from funidata_utils.sis_integration.resources import OriPersons, CodeBooks
from funidata_utils.sis_integration.scramblers.replacement_data import first_names, last_names
from tests.helpers import mock_sync_client, _get_mock_httpx_client


# You can test the real sis-integration by settings this to False
use_mock_httpx_data = True


class Diu(BaseModel):
    host: str = 'http://localhost:18080'
    proxies: dict | None = None

    def get_export_auth(self) -> tuple[str, str]:
        return 'lab.e', 'test123'


@pytest.mark.e2e
def test_generator_export_without_scramble(mock_sync_client, monkeypatch):
    if use_mock_httpx_data:
        monkeypatch.setattr(httpx_requests, "_get_httpx_client", _get_mock_httpx_client)

    _entities = export_from_sisu(
        sisu_config=Diu(),
        resource=OriPersons,
        as_generator=True,
        scramble=False
    )
    first_batch = next(_entities)
    assert len(first_batch) > 0
    # All persons have the same name in unscrambled mock dataset
    assert len({x['firstNames'] for x in first_batch}) == 1
    assert len({x['lastName'] for x in first_batch}) == 1


@pytest.mark.e2e
def test_generator_export_with_scramble(mock_sync_client, monkeypatch):
    if use_mock_httpx_data:
        monkeypatch.setattr(httpx_requests, "_get_httpx_client", _get_mock_httpx_client)

    _entities = export_from_sisu(
        sisu_config=Diu(),
        resource=OriPersons,
        as_generator=True,
        scramble=True
    )
    first_batch = next(_entities)
    assert len(first_batch) > 0

    # All persons have unique names that are a part of the replacement data
    assert len({x['firstNames'] for x in first_batch}) == 3
    assert len({x['lastName'] for x in first_batch}) == 3
    assert all(x['firstNames'] in first_names for x in first_batch)
    assert all(x['lastName'] in last_names for x in first_batch)


@pytest.mark.e2e
def test_generator_export_fails_with_scramble_for_unsupported_resource(mock_sync_client, monkeypatch):
    if use_mock_httpx_data:
        monkeypatch.setattr(httpx_requests, "_get_httpx_client", _get_mock_httpx_client)

    with pytest.raises(AttributeError):
        _entities = export_from_sisu(
            sisu_config=Diu(),
            resource=CodeBooks,
            as_generator=True,
            scramble=True
        )
        first_batch = next(_entities)


@pytest.mark.e2e
def test_regular_export_fails_with_scramble_for_unsupported_resource(mock_sync_client, monkeypatch):
    if use_mock_httpx_data:
        monkeypatch.setattr(httpx_requests, "_get_httpx_client", _get_mock_httpx_client)

    with pytest.raises(AttributeError):
        _entities = export_from_sisu(
            sisu_config=Diu(),
            resource=CodeBooks,
            as_generator=False,
            scramble=True
        )
        first_batch = next(_entities)


@pytest.mark.e2e
def test_regular_export_fails_without_scramble_for_unsupported_resource(mock_sync_client, monkeypatch):
    if use_mock_httpx_data:
        monkeypatch.setattr(httpx_requests, "_get_httpx_client", _get_mock_httpx_client)

    _entities = export_from_sisu(
        sisu_config=Diu(),
        resource=CodeBooks,
        as_generator=False,
        scramble=False
    )
    assert len(_entities) > 1
