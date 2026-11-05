# funidata-python-utils

`funidata-utils` is a Python library of utilities for integrating with Funidata products, mainly the
[Sisu](https://funidata.fi/sisu/) student information system. It is a library only. There is no CLI and no service.

It provides:

- **Sisu API integration**: export, import, patch and soft-delete entities through the Sisu integration APIs, with
  batching, pagination, parallel requests and automatic isolation of failing records.
- **Data scrambling**: deterministic anonymization of exported production data so it can be used in test
  environments while keeping references between entities intact.
- **Pydantic schemas**: typed models of Sisu entities (study rights, attainments, persons, …).
- **Config models**: Pydantic models for Sisu, database (SQLAlchemy) and AWS credentials, with secrets held as
  `SecretStr`.
- **Helpers**: SQL query helpers, JSONL reading and httpx request utilities.

Supports Python 3.11, 3.12 and 3.13.

## Installation

The package is private and not published to PyPI. Install it from the Git repository:

```bash
pip install "funidata-utils @ git+ssh://git@github.com/funidata/funidata-python-utils.git"

# with the optional SQL dependencies (SQLAlchemy, psycopg2)
pip install "funidata-utils[sql] @ git+ssh://git@github.com/funidata/funidata-python-utils.git"
```

To pin a release, append a tag, for example `...python-utils.git@<tag>`. The package version comes from Git tags.

## Usage

Import from the package, not from individual modules. The public API is re-exported through the package
`__init__.py` files.

### Configuring a Sisu connection

`SisuConfig` has two credential pairs: the **export user** for reads and the **integration user** for writes.

```python
from funidata_utils.auth import SisuConfig, BasicAuthUser

sisu = SisuConfig(
    host="https://sisu.example.fi",
    root_organisation="example-root-org-id",
    export_user=BasicAuthUser(username="export-user", password="..."),
    integration_user=BasicAuthUser(username="integration-user", password="..."),
    proxies=None,  # optional
)
```

Because the config classes are Pydantic models, they can also be loaded from JSON, environment variables or a
secrets manager with `SisuConfig.model_validate(...)`.

### Resources

Each Sisu API resource is a class in `SisResources`. It declares which endpoints the resource supports (exports,
imports, legacy imports, patches, deletes) and the batch limits for each:

```python
from funidata_utils.sis_integration import SisResources

SisResources.Attainments
SisResources.StudyRights
SisResources.CourseUnits
# ... see funidata_utils/sis_integration/resources/sis_resources.py for the full list
```

### Exporting

`export_from_sisu` pages through an export endpoint on `greatestOrdinal`. It can return the data in three ways:

```python
from funidata_utils.sis_integration import export_from_sisu, SisResources

# 1. Everything as a list
attainments = export_from_sisu(sisu, SisResources.Attainments)

# 2. Page by page, with a generator
for batch in export_from_sisu(sisu, SisResources.Attainments, as_generator=True):
    ...

# 3. Streamed to a file as JSONL, additionally scrambled for use in a test environment
with open("attainments.jsonl", "w") as fp:
    export_from_sisu(sisu, SisResources.Attainments, fp=fp, scramble=True)
```

`since_ordinal` resumes an export from a known ordinal, and `params` passes extra query parameters.
`scramble` toggles data pseudonymisation for the resource
### Importing, patching and deleting

The write operations are `async`:

```python
import asyncio
from funidata_utils.sis_integration import import_to_sisu, patch_to_sisu, soft_delete_from_sisu, SisResources

responses = asyncio.run(
    import_to_sisu(
        sisu,
        SisResources.Attainments,
        use_legacy_import=False,
        data=attainments,
        binary_search_max_depth=10,   # isolate  and retry failing records recursively until limit (0 = off)
        group_by_key="personId",      # keep a person's attainments in the same request
        max_parallel_requests=4,
    )
)
```

- **Batching**: `batch_size` defaults to the limit defined on the resource.
- **Error isolation**: when a batch returns a 4xx, the payload is split into halves recursively, using the
  `failingIds` in the response. The bad records are isolated and the rest are imported. `binary_search_max_depth`
  limits how deep the splitting goes.
- **Grouping**: `group_by_key` keeps related entities in the same request. `binary_err_search_sublists` controls
  whether the error search may split those groups.
- `patch_to_sisu` takes the same arguments.
- `soft_delete_from_sisu` sets `documentState: DELETED` on the entities. By default
  (`method_override=DeleteMethodOverride.Automatic`) it chooses the delete endpoint, a patch or an import, depending
  on what the resource supports.

Every write call returns the list of `httpx.Response` objects.

### Data scrambling

Resources that support scrambling list their scramblers in `scrambling_classes`, and `export_from_sisu(...,
scramble=True)` applies them. Scrambling is **deterministic**: values are hashed from stable keys (usually the entity
`id`) into replacement word lists. The same person gets the same fake name in every resource and every run.

> [!IMPORTANT]
> Scrambled exports **drop every field that no scrambler declares**. When Sisu adds a new field, it will be missing
> from scrambled output until it is added to the relevant scrambler's `scrambling_keys`. Declare it with the value
> `None` to pass it through unchanged.

### Schemas

```python
from funidata_utils.schemas.sisu import StudyRight, CourseUnitAttainment

study_right = StudyRight.model_validate(raw_json)
```

Entities with `documentState: ACTIVE` are fully validated. `DRAFT` and `DELETED` records are built without
validation, because they are often incomplete.

### Databases

Requires the `[sql]` extra.

```python
from funidata_utils.auth import DatabaseConfig

db = DatabaseConfig(override_connection_uri="postgresql+psycopg2://user:pwd@host:5432/db")
rows = db.get_by_statement("SELECT * FROM persons WHERE id = :id", {"id": "..."})
```

Instead of `override_connection_uri`, you can give `host`, `port`, `username`, `password`, `database`,
`sql_server_type` and `sql_driver` separately. `MariaDbConfig` is a preconfigured subclass for MariaDB.

## Development

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # editable install with all extras + test dependencies
```

### Running tests

Run pytest from the repository root, because the tests import `tests.helpers`:

```bash
pytest                      # full suite
pytest -m unit              # scrambler unit tests only
pytest -m "not e2e"         # skip tests that can target a real Sisu
pytest tests/test_export_methods.py::<test_name>   # a single test

coverage run -m pytest && coverage report
```

To run the tests against each supported Python version in Docker, the same matrix CI uses:

```bash
docker compose run --rm pytest_311
docker compose run --rm pytest_312
docker compose run --rm pytest_313
```

Notes:

- `--strict-markers` is enabled. Declare any new marker in `pyproject.toml` (existing markers: `unit`, `e2e`, `slow`).
- pytest-asyncio runs in strict mode, so async tests need `@pytest.mark.asyncio`.
- `e2e` tests use `httpx.MockTransport` by default. To run them against a real Sisu instance, set the
  `use_mock_httpx_data` flag at the top of the test file to `False`.

CI (`.github/workflows/pytest-verify.yml`) runs `pytest` on Python 3.11, 3.12 and 3.13.

### Project layout

```
funidata_utils/
├── auth/              # Pydantic config models (Sisu, database, AWS)
├── sis_integration/   # export / import / patch / delete verbs
│   └── resources/     # registry of Sisu API resources and their endpoints
├── request_utils/     # httpx helpers, incl. binary-search error isolation
├── data_scramblers/   # anonymization of exported data
├── schemas/sisu/      # Pydantic models of Sisu entities
├── database/          # SQLAlchemy helpers
├── json_tools/        # JSONL utilities
└── compat/            # Python 3.11 vs 3.12+ implementations
```

### Common tasks

- **Add a Sisu endpoint**: add a resource class to `sis_integration/resources/sis_resources.py` and export it in
  `__all__`. No other change is needed.
- **Add a scrambler**: subclass `SingletonMetaScrambler`, declare `scrambling_keys`, and add it to the resource's
  `scrambling_classes`.
- **Code that needs Python 3.12+ syntax** (PEP 695 generics, `typing.override`): put it in the `compat/` module pair
  and keep both implementations in sync.

### Conventions

- Source files start with the `Copyright (c) 2025 Funidata Oy.` header.
- Prefix branch names and commit messages with the Jira issue key, for example `BS-163: <summary>`.
- Open pull requests against `main`.
