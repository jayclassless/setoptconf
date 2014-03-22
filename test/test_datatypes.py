from decimal import Decimal

import setoptconf as soc


GOOD_SIMPLE_VALUES = (
    (soc.String, None, None),
    (soc.String, 'foo', 'foo'),
    (soc.String, '1', '1'),
    (soc.String, 1, '1'),
    (soc.String, 1.23, '1.23'),
    (soc.String, Decimal('1.23'), '1.23'),

    (soc.Integer, None, None),
    (soc.Integer, 123, 123),
    (soc.Integer, '123', 123),
    (soc.Integer, 123.45, 123),
    (soc.Integer, Decimal('123'), 123),
    (soc.Integer, Decimal('123.45'), 123),
    
    (soc.Float, None, None),
    (soc.Float, 123, 123.0),
    (soc.Float, '123', 123.0),
    (soc.Float, 123.45, 123.45),
    (soc.Float, Decimal('123'), 123.0),
    (soc.Float, Decimal('123.45'), 123.45),

    (soc.Boolean, None, None),
    (soc.Boolean, True, True),
    (soc.Boolean, False, False),
    (soc.Boolean, 'y', True),
    (soc.Boolean, 'yes', True),
    (soc.Boolean, 't', True),
    (soc.Boolean, 'true', True),
    (soc.Boolean, 'on', True),
    (soc.Boolean, '1', True),
    (soc.Boolean, '', False),
    (soc.Boolean, 'n', False),
    (soc.Boolean, 'no', False),
    (soc.Boolean, 'f', False),
    (soc.Boolean, 'false', False),
    (soc.Boolean, 'off', False),
    (soc.Boolean, '0', False),
    (soc.Boolean, 123, True),
    (soc.Boolean, 0, False),
    (soc.Boolean, 123.45, True),
)

BAD_SIMPLE_VALUES = (
    (soc.Integer, 'foo'),
    (soc.Integer, '123abc'),

    (soc.Float, 'foo'),
    (soc.Float, '123abc'),
    (soc.Float, '123.45abc'),

    (soc.Boolean, 'foo'),
)

def test_simple_sanitization():
    for datatype, in_value, out_value in GOOD_SIMPLE_VALUES:
        yield check_good_value, datatype, in_value, out_value
    for datatype, in_value in BAD_SIMPLE_VALUES:
        yield check_bad_value, datatype, in_value

def check_good_value(datatype, in_value, out_value):
    dt = datatype()
    assert dt.sanitize(in_value) == out_value
    assert dt.is_valid(in_value) is True

def check_bad_value(datatype, in_value):
    dt = datatype()
    try:
        dt.sanitize(in_value)
    except soc.DataTypeError:
        pass
    else:
        assert False, 'Invalid %s allowed: %s' % (
            datatype.__name__,
            in_value,
        )

    assert dt.is_valid(in_value) is False


GOOD_LIST_VALUES = (
    (soc.String, None, None),
    (soc.String, [], []),
    (soc.String, ['foo', 'bar'], ['foo', 'bar']),
    (soc.String, ('foo', 'bar'), ['foo', 'bar']),
    (soc.String(), ['foo', 'bar'], ['foo', 'bar']),
    (soc.String, 'foo', ['foo']),
    (soc.Integer, [123, '456'], [123, 456]),
)

BAD_LIST_VALUES = (
    (soc.Integer, ['foo'], soc.DataTypeError),
    (soc.Boolean, [True, False, 'y', 4, 'foo'], soc.DataTypeError),
    ('a', ['foo'], TypeError),
    (soc.Configuration, ['foo'], TypeError),
)

def test_list_sanitization():
    for subtype, in_value, out_value in GOOD_LIST_VALUES:
        yield check_good_list_value, subtype, in_value, out_value
    for subtype, in_value, exc in BAD_LIST_VALUES:
        yield check_bad_list_value, subtype, in_value, exc

def check_good_list_value(subtype, in_value, out_value):
    dt = soc.List(subtype)
    assert dt.sanitize(in_value) == out_value

def check_bad_list_value(subtype, in_value, exc):
    try:
        dt = soc.List(subtype)
        dt.sanitize(in_value)
    except exc:
        pass
    else:
        assert False, 'Invalid %s allowed: %s' % (
            subtype.__class__.__name__,
            in_value,
        )


GOOD_CHOICE_VALUES = (
    (soc.String, ['foo', 'bar'], None),
    (soc.String, ['foo', 'bar'], 'foo'),
    (None, ['foo', 'bar'], 'foo'),
    (soc.Integer, [1,2,3], 2),
    (soc.Integer(), [1,2,3], 2),
)

BAD_CHOICE_VALUES = (
    (soc.String, ['foo', 'bar'], 'baz', soc.DataTypeError),
    (soc.String, [1, 2, 3], 'baz', soc.DataTypeError),
    ('a', [1, 2, 3], 4, TypeError),
)

def test_choice_sanitization():
    for subtype, choices, value in GOOD_CHOICE_VALUES:
        yield check_good_choice_value, subtype, choices, value
    for subtype, choices, value, exc in BAD_CHOICE_VALUES:
        yield check_bad_choice_value, subtype, choices, value, exc

def check_good_choice_value(subtype, choices, value):
    dt = soc.Choice(choices, subtype)
    assert dt.sanitize(value) == value

def check_bad_choice_value(subtype, choices, value, exc):
    try:
        dt = soc.Choice(choices, subtype)
        dt.sanitize(value)
    except exc:
        pass
    else:
        assert False, 'Invalid choice allowed: %s' % value

