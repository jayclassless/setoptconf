
import setoptconf as soc


def make_settings1():
    settings = []
    setting = soc.StringSetting('foo')
    setting.value = 'hello'
    settings.append(setting)
    setting = soc.IntegerSetting('bar')
    setting.value = 123
    settings.append(setting)
    setting = soc.BooleanSetting('baz', default=False)
    settings.append(setting)
    return settings


def make_settings2():
    settings = []
    setting = soc.StringSetting('foo')
    setting.value = 'goodbye'
    settings.append(setting)
    setting = soc.IntegerSetting('bar')
    settings.append(setting)
    return settings


def make_settings3():
    settings = []
    setting = soc.StringSetting('foo')
    setting.value = 'happy'
    settings.append(setting)
    return settings


def test_one_level():
    config = soc.Configuration(make_settings1())

    assert len(config) == 3

    assert 'foo' in config
    assert config.foo == 'hello'
    assert config['foo'] == 'hello'

    assert 'bar' in config
    assert config.bar == 123
    assert config['bar'] == 123

    assert 'baz' in config
    assert config.baz is False
    assert config['baz'] is False


def test_two_level():
    parent = soc.Configuration(make_settings1())
    child = soc.Configuration(make_settings2(), parent=parent)

    assert len(child) == 3

    assert 'foo' in child
    assert child.foo == 'goodbye'
    assert child['foo'] == 'goodbye'

    assert 'bar' in child
    assert child.bar == 123
    assert child['bar'] == 123

    assert 'baz' in child
    assert child.baz is False
    assert child['baz'] is False


def test_three_level():
    grand_parent = soc.Configuration(make_settings1())
    parent = soc.Configuration(make_settings2(), parent=grand_parent)
    child = soc.Configuration(make_settings3(), parent=parent)

    assert len(child) == 3

    assert 'foo' in child
    assert child.foo == 'happy'
    assert child['foo'] == 'happy'

    assert 'bar' in child
    assert child.bar == 123
    assert child['bar'] == 123

    assert 'baz' in child
    assert child.baz is False
    assert child['baz'] is False


def test_missing():
    config = soc.Configuration(make_settings1())

    try:
        config['happy']
    except AttributeError:
        pass
    else:
        assert False, 'No AttributeError for missing setting'

    try:
        config.happy
    except AttributeError:
        pass
    else:
        assert False, 'No AttributeError for missing setting'

    try:
        config.validate_setting('happy')
    except AttributeError:
        pass
    else:
        assert False, 'No AttributeError for missing setting'


def test_validation():
    settings1 = make_settings1()

    parent = soc.Configuration(settings1)
    parent.validate()

    child = soc.Configuration(make_settings2(), parent=parent)
    child.validate()

    setting = soc.StringSetting('happy', required=True)
    settings1.append(setting)
    parent = soc.Configuration(settings1)
    child = soc.Configuration(make_settings2(), parent=parent)
    try:
        parent.validate()
    except soc.MissingRequiredError:
        pass
    else:
        assert False, 'No MissingRequiredError for required setting'
    try:
        child.validate()
    except soc.MissingRequiredError:
        pass
    else:
        assert False, 'No MissingRequiredError for required setting'

    setting.value = 'sad'
    parent.validate()
    child.validate()


def test_readonly():
    config = soc.Configuration(make_settings1())

    try:
        config.foo = 'qwerty'
    except soc.ReadOnlyError:
        pass
    else:
        assert False, 'Expected ReadOnlyError'

    try:
        config['foo'] = 'qwerty'
    except soc.ReadOnlyError:
        pass
    else:
        assert False, 'Expected ReadOnlyError'

    try:
        del config.foo
    except soc.ReadOnlyError:
        pass
    else:
        assert False, 'Expected ReadOnlyError'

    try:
        del config['foo']
    except soc.ReadOnlyError:
        pass
    else:
        assert False, 'Expected ReadOnlyError'

