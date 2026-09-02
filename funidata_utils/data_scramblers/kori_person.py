from .utils.key_scramblers import (
    get_scrambled_first_name, get_scrambled_last_name, get_scrambled_email,
)
from ..data_scramblers.base import SingletonMetaScrambler


class KoriPersonScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    scrambling_keys = dict(
        id=None,
        documentState=None,
        universityOrgIds=None,
        titles=None,
        firstName=[
            get_scrambled_first_name,
        ],
        lastName=[
            get_scrambled_last_name,
        ],
        emailAddress=[
            get_scrambled_email
        ],
    )
