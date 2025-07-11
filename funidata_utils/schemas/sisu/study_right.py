#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

import datetime
from typing import Optional, Literal

from pydantic import model_validator, BaseModel, field_validator, field_serializer, Field, conint, constr, PastDate

from ...schemas.sisu.common import SIS_MAX_LONG_STRING_LENGTH, OTM_ID_REGEX_PATTERN, SIS_MAX_TERSE_STRING_LENGTH


class LocalDateRange(BaseModel):
    startDate: datetime.date | None = None
    endDate: datetime.date | None = None

    @field_serializer('startDate', 'endDate')
    def serialize_dt(self, dt: datetime.date | None, _info):
        if dt is None:
            return dt
        return dt.isoformat()


class StudyRightCourseUnitSelection(BaseModel):
    localId: str
    validityPeriod: LocalDateRange | None = None
    acceptorPersonId: str | None = None
    acceptanceDate: datetime.date | None = None
    courseUnitGroupId: str

    @field_serializer('acceptanceDate')
    def serialize_dt(self, dt: datetime.date | None, _info):
        if dt is None:
            return dt
        return dt.isoformat()


class StudyRightMinorSelection(BaseModel):
    localId: str
    validityPeriod: LocalDateRange | None = None
    acceptorPersonId: str | None = None
    acceptanceDate: datetime.date | None = None
    moduleGroupId: str
    selectionState: str
    selectionType: str

    @field_serializer('validityPeriod')
    def serialize_dtr(self, val: LocalDateRange | None, _info):
        if val is None:
            return None

        if val.startDate is None and val.endDate is None:
            return None

        return val

    @field_serializer('acceptanceDate')
    def serialize_dt(self, dt: datetime.date | None, _info):
        if dt is None:
            return dt
        return dt.isoformat()


class StudyRightExtension(BaseModel):
    localId: str
    state: Literal['ACTIVE', 'DELETED']
    extensionCount: conint(ge=1, le=4)
    extensionStartDate: datetime.date
    grantDate: datetime.date
    workflowId: str | None = None
    grantReason: constr(min_length=1, max_length=SIS_MAX_LONG_STRING_LENGTH) | None
    grantedBy: str = Field(description='<MAGIC>PersonId', pattern=OTM_ID_REGEX_PATTERN)
    deleteDate: datetime.date | None = None
    deleteReason: constr(min_length=1, max_length=SIS_MAX_TERSE_STRING_LENGTH) | None
    deletedBy: str | None = Field(default=None, description='<MAGIC>PersonId', pattern=OTM_ID_REGEX_PATTERN)

    @model_validator(mode='after')
    def workflow_id_or_grant_reason_required(self):
        if self.workflowId is None and self.grantReason is None:
            raise ValueError('Either workflowId or grantReason must be specified')

        return self

    @field_serializer('grantDate', 'deleteDate', 'extensionStartDate')
    def serialize_dt(self, dt: datetime.date | None, _info):
        if dt is None:
            return dt
        return dt.isoformat()


class StudyRightCancellation(BaseModel):
    cancellationDate: PastDate
    cancellationReason: constr(min_length=1, max_length=SIS_MAX_TERSE_STRING_LENGTH)
    cancellationType: Literal[
        'RESCINDED',
        'CANCELLED_BY_ADMINISTRATION',
    ]

    @field_serializer('cancellationDate')
    def serialize_dt(self, dt: datetime.date | None, _info):
        if dt is None:
            return dt
        return dt.isoformat()


def _get_start_and_end_date_from_range(date_range: LocalDateRange | None):
    if date_range is None:
        start = datetime.date(year=1, month=1, day=1)
        end = datetime.date(year=9999, month=1, day=1)
    else:
        start = date_range.startDate or datetime.date(year=1, month=1, day=1)
        end = date_range.endDate or datetime.date(year=9999, month=1, day=1)
    return start, end


class StudyRight(BaseModel):
    id: str
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    snapshotDateTime: datetime.datetime | None
    studentId: str = Field(description='PrivatePersonId')
    educationId: str
    organisationId: str
    learningOpportunityId: str
    admissionTargetId: Optional[str] = None
    admissionIdentifier: Optional[str] = None
    decreeOnUniversityDegreesUrn: Optional[str] = None
    studyRightExpirationRulesUrn: str
    degreeRegulations: Optional[str] = None
    valid: LocalDateRange | None = None
    grantDate: str | None = None
    # studyStartDate: str < This cannot be set, sisu calculated field.
    transferOutDate: Optional[str] = None
    transferOutUniversityUrn: Optional[str] = None
    homeOrganisationUrn: Optional[str] = None
    termRegistrations: Optional[str] = None
    studyRightExtensions: Optional[list[StudyRightExtension]] = None
    studyRightCancellation: Optional[StudyRightCancellation] = None
    studyRightGraduation: Optional[dict] = None
    acceptedSelectionPath: dict
    # requestedSelectionPath: Optional[dict] = None # Causes pain and suffering this does.
    studyRightTransfer: Optional[dict] = None
    # state: < Cannot be set, sisu generated
    # statePeriods: < Cannot be set, sisu generated
    phase1MinorSelections: Optional[list[StudyRightMinorSelection]] = None
    phase2MinorSelections: Optional[list[StudyRightMinorSelection]] = None
    personalizedSelectionPath: Optional[dict] = None
    courseUnitSelections: Optional[list[StudyRightCourseUnitSelection]] = None
    moduleSelections: Optional[list] = None
    studyFieldUrn: Optional[str] = None
    phase1EducationClassificationUrn: Optional[str] = None
    phase2EducationClassificationUrn: Optional[str] = None
    phase1EducationClassificationLocked: bool = False
    phase2EducationClassificationLocked: bool = False
    fundingSourceUrn: Optional[str] = None
    phase1QualificationUrns: Optional[list] = None
    phase2QualificationUrns: Optional[list] = None
    phase1EducationLocationUrn: str
    phase2EducationLocationUrn: Optional[str] = None
    phase1InternationalContractualDegree: Optional[dict] = None
    phase2InternationalContractualDegree: Optional[dict] = None
    admissionTypeUrn: constr(pattern='(urn:code:admission-type)(:[A-z_0-9]+)*') | None = None
    codeUrns: list[constr(pattern='(urn:code)(:[A-z_0-9]+)*')]
    additionalInformation: Optional[dict] = None
    # basedOnEnrolmentRights: bool < Apparently removed from sisu model at some point in time
    cooperationNetworkRights: Optional[str] = None
    cooperationNetworkStatus: Optional[dict] = None
    schoolEducationLanguageUrn: Optional[str] = None

    @field_serializer('snapshotDateTime')
    def serialize_ssdt(self, ssdt: datetime.datetime | None, _info):
        if ssdt is None:
            return None

        return ssdt.strftime("%Y-%m-%dT%H:%M:%S")

    @model_validator(mode='after')
    def check_classification_urn_when_graduated(self):
        graduation = self.studyRightGraduation
        if not graduation:
            return self

        phase1_urn = self.phase1EducationClassificationUrn
        if not phase1_urn:
            raise ValueError("Must have classification urn if graduated")

        return self

    @model_validator(mode='after')
    def check_personalized_selection_path_matches_accepted_path(self):
        personalized_path = self.personalizedSelectionPath
        if not personalized_path:
            return self

        accepted_path = self.acceptedSelectionPath
        if not personalized_path != accepted_path:
            raise ValueError("Accepted selection path must match personalized selection path")

        return self

    @model_validator(mode='after')
    def valid_documentstate_active_validator(self):
        if self.documentState != 'ACTIVE':
            return self

        if self.valid is None:
            raise ValueError("valid is required when ACTIVE")

        if self.valid.startDate is None:
            raise ValueError("Start date must not be None when ACTIVE")

        return self

    @model_validator(mode='after')
    def grant_date_required_if_active(self):
        if self.documentState != 'ACTIVE':
            return self

        if self.grantDate is None:
            raise ValueError("grantDate must not be None when ACTIVE")

        return self

    @model_validator(mode='after')
    def non_overlapping_cu_selections(self):
        cu_selections = self.courseUnitSelections

        if not cu_selections:
            return self

        overlaps = []

        # Pain and suffering to be had
        for index, cu_selection in enumerate(cu_selections):
            start, end = _get_start_and_end_date_from_range(cu_selection.validityPeriod)

            for cu_sel_2 in cu_selections[index + 1:]:
                if cu_selection.courseUnitGroupId != cu_sel_2.courseUnitGroupId:
                    continue

                start2, end2 = _get_start_and_end_date_from_range(cu_sel_2.validityPeriod)

                # https://stackoverflow.com/a/9044111
                latest_start = max(start, start2)
                earliest_end = min(end, end2)
                delta = (earliest_end - latest_start).days
                overlap = max(0, delta)

                if overlap > 0:
                    overlaps.append([cu_selection, cu_sel_2])

        if overlaps:
            raise ValueError(f"Overlapping course unit selections: {overlaps}")

        return self

    @field_validator("studyRightExtensions")
    def ext_contains_no_nulls(cls, val):
        if not val:
            return None

        for _val in val:
            if _val is None:
                raise ValueError('Extensions may not contain nulls', val, _val)

        return val

    @field_validator("courseUnitSelections")
    def cu_selection_validator(cls, val: list):
        if any(entry is None for entry in val):
            raise ValueError("courseUnitSelections may not contain nulls")

        return val

    @field_validator("phase1MinorSelections", "phase2MinorSelections")
    def minor_selection_start_date_required(cls, val: list | None):
        if isinstance(val, list):
            for entry in val:
                val_per = entry.validityPeriod
                if val_per is None:
                    continue
                if val_per.startDate is None and val_per.endDate is not None:
                    raise ValueError("MinorSelection must have startDate", entry)

        return val

    @field_validator("phase1MinorSelections", "phase2MinorSelections")
    def minor_selection_duplicates_not_allowed(cls, val: list[StudyRightMinorSelection] | None):
        group_ids = set()
        local_ids = set()
        if isinstance(val, list):
            for entry in val:
                if entry.moduleGroupId in group_ids:
                    raise ValueError(
                        "MinorSelections may not contain duplicate module group ids",
                        entry.moduleGroupId
                    )
                group_ids.add(entry.moduleGroupId)

                if entry.localId in local_ids:
                    raise ValueError(
                        "MinorSelections may not contain duplicate localIds",
                        entry.localId
                    )
                local_ids.add(entry.localId)

        return val

    @field_serializer('studyRightGraduation')
    def custom_serialize_sr_graduation(self, sr_grad: dict | None, _info):
        if isinstance(sr_grad, dict):
            if sr_grad.get('phase1GraduationDate') is None and sr_grad.get('phase2GraduationDate') is None:
                return None

        return sr_grad
