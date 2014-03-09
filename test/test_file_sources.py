import atexit
import os.path
import tempfile

import setoptconf as soc


_TEMPFILES = []

def make_temp(content):
    name = tempfile.mkstemp()[1]
    fp = open(name, 'w')
    fp.write(content)
    fp.close()
    _TEMPFILES.append(name)
    return name

def cleanup_temps():
    for temp in _TEMPFILES:
        if os.path.exists(temp):
            os.remove(temp)

atexit.register(cleanup_temps)


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
    return settings


def test_directory_modifier():
    file1 = make_temp("""
[mytest]
foo = hello
bar = 123
""")

    source = soc.ConfigFileSource(
        [file1, soc.HomeDirectory('foobar')],
        section='mytest'
    )
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is False
    assert config.happy is None


def test_configfile():
    file1 = make_temp('')

    source = soc.ConfigFileSource(file1, section='mytest')
    config = source.get_config(make_settings())

    assert config.foo is None
    assert config.bar is None
    assert config.baz is False
    assert config.happy is None

    file2 = make_temp("""
[mytest]
foo = hello
bar = 123
""")

    source = soc.ConfigFileSource(file2, section='mytest')
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is False
    assert config.happy is None

    file3 = make_temp("""
[mytest]
foo = hello
bar: 123
baz = true
happy:foo,"bar"
""")

    source = soc.ConfigFileSource(file3, section='mytest')
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is True
    assert config.happy == ['foo', 'bar']

    file4 = make_temp("""
[mytest]
foo = goodbye
""")

    source = soc.ConfigFileSource([file3,file4], section='mytest')
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is True
    assert config.happy == ['foo', 'bar']

    source = soc.ConfigFileSource([file4,file3], section='mytest', combine=True)
    config = source.get_config(make_settings())

    assert config.foo == 'goodbye'
    assert config.bar == 123
    assert config.baz is True
    assert config.happy == ['foo', 'bar']

    try:
        source = soc.ConfigFileSource(123, section='mytest')
    except TypeError:
        pass
    else:
        assert False, 'Expected TypeError for bogus file name'

    try:
        source = soc.ConfigFileSource(['foobar', 123], section='mytest')
    except TypeError:
        pass
    else:
        assert False, 'Expected TypeError for bogus file name'


def test_jsonfile():
    file1 = make_temp('')

    source = soc.JsonFileSource(file1)
    config = source.get_config(make_settings())

    assert config.foo is None
    assert config.bar is None
    assert config.baz is False
    assert config.happy is None

    file2 = make_temp("""
{
    "foo": "hello",
    "bar": 123
}
""")

    source = soc.JsonFileSource(file2)
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is False
    assert config.happy is None

    file3 = make_temp("""
{
    "foo": "hello",
    "bar": 123,
    "baz": true,
    "happy": ["foo", "bar"]
}
""")

    source = soc.JsonFileSource(file3)
    config = source.get_config(make_settings())

    assert config.foo == 'hello'
    assert config.bar == 123
    assert config.baz is True
    assert config.happy == ['foo', 'bar']

    file4 = make_temp('{}')

    source = soc.JsonFileSource(file4)
    config = source.get_config(make_settings())

    assert config.foo is None
    assert config.bar is None
    assert config.baz is False
    assert config.happy is None

    file5 = make_temp('"foo"')

    source = soc.JsonFileSource(file5)
    try:
        config = source.get_config(make_settings())
    except TypeError:
        pass
    else:
        assert False, 'Expected TypeError for non-objects'


if hasattr(soc, 'YamlFileSource'):
    def test_yamlfile():
        file1 = make_temp('')

        source = soc.YamlFileSource(file1)
        config = source.get_config(make_settings())

        assert config.foo is None
        assert config.bar is None
        assert config.baz is False
        assert config.happy is None

        file2 = make_temp("""
foo: hello
bar: 123
""")

        source = soc.YamlFileSource(file2)
        config = source.get_config(make_settings())

        assert config.foo == 'hello'
        assert config.bar == 123
        assert config.baz is False
        assert config.happy is None

        file3 = make_temp("""
foo: hello
bar: 123
baz: true
happy:
  - foo
  - bar
""")

        source = soc.YamlFileSource(file3)
        config = source.get_config(make_settings())

        assert config.foo == 'hello'
        assert config.bar == 123
        assert config.baz is True
        assert config.happy == ['foo', 'bar']

        file4 = make_temp('{}')

        source = soc.YamlFileSource(file4)
        config = source.get_config(make_settings())

        assert config.foo is None
        assert config.bar is None
        assert config.baz is False
        assert config.happy is None

        file5 = make_temp('"foo"')

        source = soc.YamlFileSource(file5)
        try:
            config = source.get_config(make_settings())
        except TypeError:
            pass
        else:
            assert False, 'Expected TypeError for non-objects'

