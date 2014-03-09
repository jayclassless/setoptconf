import setoptconf as soc


def test_home_directory():
    test = soc.HomeDirectory('foo.bar')
    result = test()

    # Can't really predict the output, as it's environment-dependent.
    # Just make sure we have something that looks like a path to our file.
    assert result.startswith('/')
    assert result.endswith('foo.bar')


def test_config_directory():
    test = soc.ConfigDirectory('foo.bar')
    result = test()

    # Can't really predict the output, as it's environment-dependent.
    # Just make sure we have something that looks like a path to our file.
    assert result.startswith('/')
    assert result.endswith('foo.bar')

