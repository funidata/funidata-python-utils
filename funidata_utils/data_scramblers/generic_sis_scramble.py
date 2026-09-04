import sys


if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

from funidata_utils.data_scramblers.base import SingletonMetaScrambler
from funidata_utils.utils import update_inner_dictionary_key


class SisMetadataScrambler(SingletonMetaScrambler):
    scrambling_keys = dict(
        metadata=[
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='metadata.createdBy',
                    new_value='Lorem'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='metadata.lastModifiedBy',
                    new_value='Ipsum'
                )
            ),
        ],
    )


class UnprocessedKeysDropperScrambler(SingletonMetaScrambler):
    scrambling_keys = {}

    def __init__(self, loggable_keys: set[str]):
        self._loggable_keys = loggable_keys

    # Instance method override to provide access to self._loggable_keys, and also provide different scrambling logic from other classes
    @override
    def scramble(self, entity: dict, processed_keys: set) -> dict:  # noqa: instance method signature does not match cls method
        """ Pops any keys that are not present in processed_keys """
        entity_keys = set(entity.keys())
        _keys = set()
        for key in entity_keys:
            if key not in processed_keys:
                _keys.add(key)
                entity.pop(key)

        _keys_diff = _keys.difference(self._loggable_keys)
        if _keys_diff:
            self._loggable_keys |= _keys_diff

        return entity
