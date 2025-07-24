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
from .buildings import Building
from .curriculum_period import CurriculumPeriod
from .grade_scales import (GradeScale, Grade)
from .qualifications import Qualification
