import os

import setoptconf as soc


def make_settings():
    settings = []
    setting = soc.StringSetting('foo')
    settings.append(setting)
    setting = soc.IntegerSetting('bar')
    settings.append(setting)
    setting = soc.BooleanSetting('baz', default=False)
    settings.append(setting)
    setting = soc.ListSetting('happy', soc.String)
    settings.append(setting)
    setting = soc.ChoiceSetting('fuzziness', ['fuzzy', 'bare'], soc.String)
    settings.append(setting)
    return settings


class MyConfig:
    foo = 'hello'
    bar = 123

class MyFullConfig(MyConfig):
    baz = True
    happy = ['foo', 'bar']
    fuzziness = 'bare'

def test_object_source():
    source = soc.ObjectSource(MyConfig)
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is False
    assert config.happy is None
    assert config.fuzziness is None

    source = soc.ObjectSource(MyFullConfig)
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is True
    assert config.happy == ['foo', 'bar']
    assert config.fuzziness == 'bare'


def test_mapping_source():
    mapping = {
        'foo': 'hello',
        'bar': 123,
    }
    source = soc.MappingSource(mapping)
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is False
    assert config.happy is None
    assert config.fuzziness is None

    mapping['baz'] = True
    mapping['happy'] = ['foo', 'bar']
    mapping['fuzziness'] = 'bare'
    source = soc.MappingSource(mapping)
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is True
    assert config.happy == ['foo', 'bar']
    assert config.fuzziness == 'bare'


def test_environment_source():
    source = soc.EnvironmentVariableSource()
    config = source.get_config(make_settings())

    assert config.foo is None
    assert config.bar is None
    assert config.baz is False
    assert config.happy is None
    assert config.fuzziness is None
    
    os.environ['MYTEST_FOO'] = 'hello'
    os.environ['MYTEST_BAR'] = '123'
    os.environ['MYTEST_HAPPY'] = ''
    source = soc.EnvironmentVariableSource('mytest')
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is False
    assert config.happy == []
    assert config.fuzziness is None

    os.environ['MYTEST_BAZ'] = 'yes'
    os.environ['MYTEST_HAPPY'] = 'foo,"bar"'
    os.environ['MYTEST_FUZZINESS'] = 'bare'
    source = soc.EnvironmentVariableSource('mytest')
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is True
    assert config.happy == ['foo', 'bar']
    assert config.fuzziness == 'bare'


def test_commandline_source():
    source = soc.CommandLineSource('--foo=hello --bar=123')
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is False
    assert config.happy is None
    assert config.fuzziness is None

    source = soc.CommandLineSource('--foo=hello --bar=123 --baz --happy=foo --happy=bar --fuzziness=bare')
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is True
    assert config.happy == ['foo', 'bar']
    assert config.fuzziness == 'bare'

    source = soc.CommandLineSource(['--foo=hello','--bar=123','--baz','--happy=foo','--happy=bar','--fuzziness=bare'])
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is True
    assert config.happy == ['foo', 'bar']
    assert config.fuzziness == 'bare'

    try:
        source = soc.CommandLineSource(123)
    except TypeError:
        pass
    else:
        assert False, 'Expected TypeError for bogus arguments'

    options = {
        'foo': {
            'flags': ['--something'],
        },
        'bar': {
            'flags': ['-z', '--zoo'],
        },
    }
    source = soc.CommandLineSource('--something=hello -z=123', options=options)
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is False
    assert config.happy is None
    assert config.fuzziness is None

    class FakeManager(object):
        name = 'fake'

    positional = (
        ('red', {}),
        ('blue', {'type': int}),
    )
    source = soc.CommandLineSource('--foo=hello --bar=123 myred 4', positional=positional)
    mgr = FakeManager()
    config = source.get_config(make_settings(), manager=mgr)

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is False
    assert config.happy is None
    assert config.fuzziness is None
    assert mgr.arguments['red'] == 'myred'
    assert mgr.arguments['blue'] == 4

