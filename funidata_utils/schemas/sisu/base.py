from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, model_validator


class HashableBaseModel(BaseModel):
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class SisBase(HashableBaseModel):
    """
        Base model for depicting Sisu entities, with a custom model validator for ACTIVE class vs DRAFT/DELETED
    """

    model_config = ConfigDict(from_attributes=True)

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
