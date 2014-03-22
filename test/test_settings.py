from decimal import Decimal

import setoptconf as soc


GOOD_NAMES = (
    'foo',
    'foo_bar',
    'foo123',
    'foo_bar_baz',
)

BAD_NAMES = (
    '_foo',
    '1foo',
    'FOO',
    'foo_',
    'foo__bar',
    'foo-bar',
)

def test_name():
    for name in GOOD_NAMES:
        yield check_good_name, name
    for name in BAD_NAMES:
        yield check_bad_name, name

def check_good_name(name):
    setting = soc.StringSetting(name)

def check_bad_name(name):
    try:
        setting = soc.StringSetting(name)
    except soc.NamingError:
        pass
    else:
        assert False, 'Invalid name allowed: %s' % name


def test_list_setting():
    setting = soc.ListSetting('foo', soc.String)

    assert setting.name == 'foo'

    setting.value = ['bar', 'baz']

    assert setting.value == ['bar', 'baz']


def test_choice_setting():
    setting = soc.ChoiceSetting('foo', ['bar', 'baz'], soc.String)

    assert setting.name == 'foo'

    setting.value = 'baz'

    assert setting.value == 'baz'

