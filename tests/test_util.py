import pytest
from funidata_utils.utils import group_by


def test_group_by():
    data = [dict(id=1, type=1), dict(id=2, type=1), dict(id=3, type=2)]

    grouping = group_by(data, lambda x: x['type'] == 1)

    assert grouping[1] == [dict(id=1, type=1), dict(id=2, type=1)]


@pytest.mark.unit
def test_update_inner_dictionary_key_skip_does_not_evaluate_new_value_for_missing_key():
    from funidata_utils.utils import update_inner_dictionary_key

    def raising_scrambler(entity, **kwargs):
        raise AssertionError("new_value must not be evaluated when the key is missing and handler is 'skip'")

    entity = {"root": {"other": "value"}}

    update_inner_dictionary_key(
        entity,
        dot_separated_key="root.leaf",
        new_value=(raising_scrambler, dict(key="leaf")),
        missing_key_handler="skip",
    )

    assert entity == {"root": {"other": "value"}}


@pytest.mark.unit
def test_update_inner_dictionary_key_applies_callable_to_each_list_item():
    from funidata_utils.utils import update_inner_dictionary_key

    entity = {"root": {"drafts": [{"name": "a"}, None, {"name": "b"}]}}

    update_inner_dictionary_key(
        entity,
        dot_separated_key="root.drafts",
        new_value=lambda draft: draft | {"name": "scrambled"},
        missing_key_handler="skip",
    )

    assert entity == {"root": {"drafts": [{"name": "scrambled"}, None, {"name": "scrambled"}]}}
