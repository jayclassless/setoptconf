import os

import setoptconf as soc


class Blah(object):
    foo = 'a'

os.environ['TESTME_BAR'] = '123'

mgr = soc.ConfigurationManager('testme')
mgr.add(soc.StringSetting('foo'))
mgr.add(soc.IntegerSetting('bar', required=True))
mgr.add(soc.BooleanSetting('baz', default=True))

config = mgr.retrieve(
    soc.EnvironmentVariableSource,
    soc.ObjectSource(Blah),
    soc.MappingSource({'baz': False}),
)

assert config.foo == 'a'
assert config.bar == 123
assert config.baz is False


try:
    mgr.add('blah')
except TypeError:
    pass
else:
    assert False, 'Expected TypeError for bogus Setting'


try:
    config = mgr.retrieve(
        soc.EnvironmentVariableSource,
        'foo',
    )
except TypeError:
    pass
else:
    assert False, 'Expected TypeError for bogus Source'

