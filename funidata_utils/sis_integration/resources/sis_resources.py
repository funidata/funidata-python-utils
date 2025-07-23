#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from .schemas import SisImport, SisExport
from re import sub


_DEFAULT_EXPORT_LIMIT = 2500
_DEFAULT_IMPORT_LIMIT = 1500

__all__ = [
    'OriPersons',
    'AccessRolePersonAssignments',
    'Attainments',
    'StudyRights',
    'TermRegistrations',
    'Thesis',
    'MobilityPeriods',
    'StudyRightPrimalities',
    'Organisations',
    'CourseUnits',
    'Educations',
    'Modules',
    'KoriPersons',
    'StudyYearTemplates',
    'CodeBooks',
    'CurriculumPeriods',
    'AssessmentItems',
    'Buildings',
    'Qualifications',
    'GradeScales',
]


class BaseMeta(type):
    @staticmethod
    def _snake_case_ify(input: str):
        input_with_spaces = sub('([a-z])([A-Z])', r'\1 \2', input)
        return input_with_spaces.lower().replace(' ', '_')

    def __repr__(self):
        return f'{self._snake_case_ify(self.__name__)}'


class BaseResource(metaclass=BaseMeta):
    pass


class OriPersons(BaseResource):
    imports = SisImport(
        endpoint='/ori/api/persons/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    patches = SisImport(
        endpoint='/ori/api/persons/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/persons/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class AccessRolePersonAssignments(BaseResource):
    imports = SisImport(
        endpoint='/ori/api/access-roles-person-assignments/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/access-roles-person-assignments/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class Attainments(BaseResource):
    imports = SisImport(
        endpoint='/ori/api/attainments/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    legacy_imports = SisImport(
        endpoint='/ori/api/attainments/v1/import/legacy',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    patches = SisImport(
        endpoint='/ori/api/attainments/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    legacy_patches = SisImport(
        endpoint='/ori/api/attainments/v1/import/legacy',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/attainments/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class StudyRights(BaseResource):
    imports = SisImport(
        endpoint='/ori/api/study-rights/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    patches = SisImport(
        endpoint='/ori/api/study-rights/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/study-rights/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class TermRegistrations(BaseResource):
    imports = SisImport(
        endpoint='/ori/api/term-registrations/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    patches = SisImport(
        endpoint='/ori/api/term-registrations/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/term-registrations/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class Thesis(BaseResource):
    imports = SisImport(
        endpoint='/ori/api/thesis/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/thesis/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class MobilityPeriods(BaseResource):
    imports = SisImport(
        endpoint='/ori/api/mobility-periods/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/mobility-periods/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class StudyRightPrimalities(BaseResource):
    imports = SisImport(
        endpoint='/ori/api/study-right-primalities/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/ori/api/study-right-primalities/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class Organisations(BaseResource):
    imports = SisImport(
        endpoint='/kori/api/organisations/v2/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/organisations/v2/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class CourseUnits(BaseResource):
    imports = SisImport(
        endpoint='/kori/api/course-units/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    legacy_imports = SisImport(
        endpoint='/ori/api/course-units/v1/import/legacy',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    patches = SisImport(
        endpoint='/kori/api/course-units/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    legacy_patches = SisImport(
        endpoint='/ori/api/course-units/v1/import/legacy',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/course-units/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class Educations(BaseResource):
    imports = SisImport(
        endpoint='/kori/api/educations/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    legacy_imports = SisImport(
        endpoint='/kori/api/educations/v1/import/legacy',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/educations/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class Modules(BaseResource):
    imports = SisImport(
        endpoint='/kori/api/modules/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    legacy_imports = SisImport(
        endpoint='/kori/api/modules/v1/import/legacy',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    patches = SisImport(
        endpoint='/kori/api/modules/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    legacy_patches = SisImport(
        endpoint='/kori/api/modules/v1/import/legacy',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/modules/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class KoriPersons(BaseResource):
    imports = SisImport(
        endpoint='/kori/api/persons/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/persons/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class StudyYearTemplates(BaseResource):
    imports = SisImport(
        endpoint='/kori/api/study-year-templates/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/study-year-templates/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class CodeBooks(BaseResource):
    exports = SisExport(
        endpoint='/kori/api/codebooks/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class CurriculumPeriods(BaseResource):
    imports = SisImport(
        endpoint='/kori/api/curriculum-periods/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/curriculum-periods/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class AssessmentItems(BaseResource):
    imports = SisImport(
        endpoint='/kori/api/assessment-items/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/assessment-items/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class Buildings(BaseResource):
    imports = SisImport(
        endpoint='/kori/api/buildings/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/buildings/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class Qualifications(BaseResource):
    imports = SisImport(
        endpoint='/kori/api/qualifications/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/qualifications/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )


class GradeScales(BaseResource):
    imports = SisImport(
        endpoint='/kori/api/grade-scales/v1/import',
        default_import_limit=_DEFAULT_IMPORT_LIMIT,
    )
    exports = SisExport(
        endpoint='/kori/api/grade-scales/v1/export',
        default_export_limit=_DEFAULT_EXPORT_LIMIT,
    )
