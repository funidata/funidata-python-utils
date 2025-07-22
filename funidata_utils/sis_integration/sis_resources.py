#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from pydantic import BaseModel, conint


_DEFAULT_EXPORT_LIMIT = 2500


class SisExport(BaseModel):
    endpoint: str
    default_export_limit: conint(ge=1, le=5000)


class SisImport(BaseModel):
    endpoint: str
    default_import_limit: conint(ge=1, le=5000) = 1500


class OriPersons:
    imports = SisImport(
        endpoint='/ori/api/persons/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    legacy_imports = SisImport(
        endpoint='/ori/api/persons/v1/import/legacy',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    patches = SisImport(
        endpoint='/ori/api/persons/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/persons/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class AccessRolePersonAssignments:
    imports = SisImport(
        endpoint='/ori/api/access-roles-person-assignments/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/access-roles-person-assignments/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class Attainments:
    imports = SisImport(
        endpoint='/ori/api/attainments/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/attainments/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class StudyRights:
    imports = SisImport(
        endpoint='/ori/api/study-rights/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/study-rights/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class TermRegistrations:
    imports = SisImport(
        endpoint='/ori/api/term-registrations/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/term-registrations/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class Thesis:
    imports = SisImport(
        endpoint='/ori/api/thesis/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/thesis/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class MobilityPeriods:
    imports = SisImport(
        endpoint='/ori/api/mobility-periods/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/mobility-periods/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class StudyRightPrimalities:
    imports = SisImport(
        endpoint='/ori/api/study-right-primalities/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/study-right-primalities/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class Organisations:
    imports = SisImport(
        endpoint='/kori/api/organisations/v2/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/organisations/v2/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class CourseUnits:
    imports = SisImport(
        endpoint='/kori/api/course-units/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/course-units/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class Educations:
    imports = SisImport(
        endpoint='/kori/api/educations/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/educations/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class Modules:
    imports = SisImport(
        endpoint='/kori/api/modules/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/modules/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class KoriPersons:
    imports = SisImport(
        endpoint='/kori/api/persons/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/persons/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class StudyYearTemplates:
    imports = SisImport(
        endpoint='/kori/api/study-year-templates/v1/import',
        default_import_limit=_DEFAULT_EXPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/study-year-templates/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )
