from pydantic import BaseModel, constr


class HashableBaseModel(BaseModel):
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class LocalizedString(HashableBaseModel):
    fi: str | None = None
    en: str | None = None
    sv: str | None = None


SIS_MAX_VERY_LONG_STRING_LENGTH = 65000
SIS_MAX_LONG_STRING_LENGTH = 8000
SIS_MAX_MEDIUM_STRING_LENGTH = 1024
SIS_MAX_TERSE_STRING_LENGTH = 255
SIS_MAX_SHORT_STRING_LENGTH = 100

SIS_MAX_TWEET_LENGTH = 160

SIS_MAX_VERY_LARGE_SET_SIZE = 20000
SIS_MAX_BIG_SET_SIZE = 4000
SIS_MAX_MEDIUM_SET_SIZE = 200
SIS_MAX_SMALL_SET_SIZE = 20

OTM_ID_REGEX_PATTERN = '([a-zA-Z]{2,5})-[A-Za-z0-9_\\-]{1,58}'
OTM_ID_REGEX_VALIDATED_STR = constr(pattern=OTM_ID_REGEX_PATTERN)
