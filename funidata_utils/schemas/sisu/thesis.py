import datetime
from typing import Literal

from pydantic import BaseModel, field_serializer, Field, constr, field_validator, conset

from ...schemas.sisu import LocalizedString
from ...schemas.sisu.attainment import PersonWithAttainmentAcceptorType, OrganisationRoleShareBase
from ...utils import group_by


class Thesis(BaseModel):
    id: str
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    personId: str = Field(description='PrivatePersonId')
    attainmentId: str | None = None
    title: LocalizedString  # This is technically annotated as optional, but lets not do that
    subject: LocalizedString | None = None
    thesisTypeUrn: constr(pattern='(urn:code:thesis-type)(:[A-z_0-9]+)*')
    responsibilityInfos: conset(PersonWithAttainmentAcceptorType, min_length=1)
    organisations: conset(OrganisationRoleShareBase, min_length=1) | None = None
    courseUnitId: str
    courseUnitGroupId: str
    state: Literal['ATTAINED']
    publicInspectionDate: datetime.date | None = None
    commissionType: Literal['COMMISSION', 'NONE']

    @field_validator("organisations")
    def has_valid_set_of_organisation_shares(cls, val: list[OrganisationRoleShareBase], _info):
        if val is None:
            return val

        orgs_by_role_urn = group_by(
            val, key=lambda x: x.roleUrn
        )
        for urn, orgs in orgs_by_role_urn.items():
            if sum(_org.share for _org in orgs) != 1:
                raise ValueError("Sum of shares must be 1 for each roleUrn")
        return val

    @field_serializer('publicInspectionDate')
    def date_as_isoformat(self, val: datetime.date | None, _info):
        if val is None:
            return None

        return val.isoformat()

    @field_serializer('organisations', 'responsibilityInfos')
    def organisations_as_list(self, val: set[OrganisationRoleShareBase] | None, _info):
        if val is None:
            return None

        return list(val)
