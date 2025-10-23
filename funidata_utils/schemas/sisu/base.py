import datetime
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, model_validator, Field


class HashableBaseModel(BaseModel):
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class CommonBase(HashableBaseModel):
    """
        Base model for depicting common pydantic models from attributes
    """

    model_config = ConfigDict(from_attributes=True)


class SisMetadata(CommonBase):
    revision: int
    createdBy: str | None
    createdOn: datetime.datetime | None = None
    lastModifiedBy: str | None = None
    lastModifiedOn: datetime.datetime | None = None
    modificationOrdinal: int


class SisBase(CommonBase):
    """
        Base model for depicting top level Sisu entities, with a custom model validator for ACTIVE class vs DRAFT/DELETED
    """
    metadata: SisMetadata | None = Field(
        default=None,
        exclude=True,
        description="Read-only - Present when exported from sisu, not meant to be initialized separately"
    )

    @model_validator(mode='wrap')
    @classmethod
    def model_validate_document_state_active(cls, data, handler) -> Self:
        """
            Basically:
                run the default handler for document state ACTIVE
                run model_construct for DRAFT and DELETED
        """

        if 'documentState' in data:
            match data['documentState']:
                case 'ACTIVE':
                    return handler(data)
                case 'DRAFT' | 'DELETED':
                    return cls.model_construct(**data)
                case _:
                    raise Exception(f'Class not supported for documentstate: {data["documentState"]}')
        else:
            return handler(data)
