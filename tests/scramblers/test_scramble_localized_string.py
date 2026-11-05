import pytest

from funidata_utils.data_scramblers.utils.generic_scrambling import scramble_localized_string

WEIGHTS = [
    ({'fi': 'Lorem fi', 'sv': 'Lorem sv', 'en': 'Lorem en'}, 1000),
    ({'fi': 'Pallerojumppa'}, 42),
]
FI_ONLY_WEIGHTS = [({'fi': 'placeholder'}, 1)]


@pytest.mark.unit
@pytest.mark.parametrize("original", [
    {'fi': 'suomeksi', 'sv': 'på svenska', 'en': 'in english'},
    {'fi': 'suomeksi', 'sv': 'på svenska'},
    {'en': 'in english'},
])
def test_scramble_localized_string_keeps_original_language_keys(original):
    entity = {'id': 'otm-1', 'reason': original}

    scrambled = scramble_localized_string(entity, 'reason', weights=WEIGHTS, scramble_seed_key='otm-1')

    assert set(scrambled) == set(original)
    for lang, value in original.items():
        assert isinstance(scrambled[lang], str) and scrambled[lang]
        assert scrambled[lang] != value


@pytest.mark.unit
def test_scramble_localized_string_preserves_falsy_language_values():
    entity = {'reason': {'fi': 'suomeksi', 'sv': None, 'en': ''}}

    scrambled = scramble_localized_string(entity, 'reason', weights=WEIGHTS, scramble_seed_key='seed')

    assert scrambled['fi'] != 'suomeksi'
    assert scrambled['sv'] is None
    assert scrambled['en'] == ''


@pytest.mark.unit
def test_scramble_localized_string_falls_back_for_languages_missing_from_weights():
    entity = {'reason': {'fi': 'suomeksi', 'sv': 'på svenska', 'en': 'in english'}}

    scrambled = scramble_localized_string(entity, 'reason', weights=FI_ONLY_WEIGHTS, scramble_seed_key='seed')

    assert scrambled == {'fi': 'placeholder', 'sv': 'placeholder (sv)', 'en': 'placeholder (en)'}


@pytest.mark.unit
def test_scramble_localized_string_is_deterministic_for_same_seed():
    entity = {'reason': {'fi': 'suomeksi', 'en': 'in english'}}

    first = scramble_localized_string(entity, 'reason', weights=WEIGHTS, scramble_seed_key='same')
    second = scramble_localized_string(entity, 'reason', weights=WEIGHTS, scramble_seed_key='same')

    assert first == second


@pytest.mark.unit
def test_scramble_localized_string_uses_original_value_as_seed_when_no_seed_given():
    entity = {'reason': {'fi': 'suomeksi'}}

    first = scramble_localized_string(entity, 'reason', weights=WEIGHTS)
    second = scramble_localized_string(entity, 'reason', weights=WEIGHTS)

    assert first == second
    assert first['fi'] != 'suomeksi'


@pytest.mark.unit
@pytest.mark.parametrize("original", [None, {}])
def test_scramble_localized_string_returns_none_for_empty_values(original):
    entity = {'reason': original}

    assert scramble_localized_string(entity, 'reason', weights=WEIGHTS, scramble_seed_key='seed') is None


@pytest.mark.unit
def test_scramble_localized_string_skips_missing_key():
    entity = {'other': 'value'}

    assert scramble_localized_string(entity, 'reason', weights=WEIGHTS, missing_key_handler='skip') is None


@pytest.mark.unit
def test_scramble_localized_string_raises_on_missing_key_by_default():
    entity = {'other': 'value'}

    with pytest.raises(KeyError):
        scramble_localized_string(entity, 'reason', weights=WEIGHTS)
