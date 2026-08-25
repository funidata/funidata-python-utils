import pytest

from funidata_utils.sis_integration.protocols import SupportsExportAuthentication
from funidata_utils.sis_integration.exports import export_from_sisu
from funidata_utils.sis_integration.resources import StudyRights, Buildings, OriPersons, CodeBooks
from pydantic import BaseModel


class Diu(BaseModel):
    host: str = 'http://localhost:18080'
    proxies: dict | None = None

    def get_export_auth(self) -> tuple[str, str]:
        return 'lab.e', 'test123'


@pytest.mark.e2e
def test_generator_export_without_scramble():
    _entities = export_from_sisu(
        sisu_config=Diu(),
        resource=OriPersons,
        as_generator=True,
        scramble=False
    )
    first_batch = next(_entities)
    assert len(first_batch) > 0


@pytest.mark.e2e
def test_generator_export_with_scramble():
    _entities = export_from_sisu(
        sisu_config=Diu(),
        resource=OriPersons,
        as_generator=True,
        scramble=True
    )
    first_batch = next(_entities)
    assert len(first_batch) > 0


@pytest.mark.e2e
def test_generator_export_fails_with_scramble_for_unsupported_resource():
    with pytest.raises(AttributeError):
        _entities = export_from_sisu(
            sisu_config=Diu(),
            resource=CodeBooks,
            as_generator=True,
            scramble=True
        )
        first_batch = next(_entities)


@pytest.mark.e2e
def test_regular_export_fails_with_scramble_for_unsupported_resource():
    with pytest.raises(AttributeError):
        _entities = export_from_sisu(
            sisu_config=Diu(),
            resource=CodeBooks,
            as_generator=False,
            scramble=True
        )
        first_batch = next(_entities)


@pytest.mark.e2e
def test_regular_export_fails_without_scramble_for_unsupported_resource():
    _entities = export_from_sisu(
        sisu_config=Diu(),
        resource=CodeBooks,
        as_generator=False,
        scramble=False
    )
    assert len(_entities) > 1
