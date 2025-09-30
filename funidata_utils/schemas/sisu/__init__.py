#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

from .study_right import (
    StudyRight,
    StudyRightExtension,
    StudyRightCancellation,
    StudyRightCourseUnitSelection,
    StudyRightMinorSelection,
)
from .common import LocalizedString
from .attainment import (
    CourseUnitAttainment,
    CustomCourseUnitAttainment,
    CustomModuleAttainment,
    DegreeProgrammeAttainment,
)
from .mobility_period import MobilityPeriod
from .thesis import Thesis
from .private_person import PrivatePerson
from .study_year_template import (
    StudyYearTemplate,
    StudyPeriodTemplate,
    StudyTermTemplate,
)
from .assessment_item import AssessmentItem
from .building import Building
from .curriculum_period import CurriculumPeriod
from .grade_scale import (GradeScale, Grade)
from .qualification import Qualification
from .organisation import Organisation
from .course_unit import CourseUnit
from .module import (
    Module,
    StudyModule,
    DegreeProgramme,
    GroupingModule,
    ModuleTypeAdapter,
)
