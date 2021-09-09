==========
setoptconf
==========

.. image:: https://github.com/jayclassless/setoptconf/workflows/Test/badge.svg
   :target: https://github.com/jayclassless/setoptconf/actions

``setoptconf`` is a Python library that can be used to retrieve program settings
from a variety of common sources:

* Command Line
* Environment Variables
* INI Files
* JSON Files
* YAML Files
* Python Objects/Modules

The goal of this project is to define your desired settings in a simple and
consistent way, and then point setoptconf at as many of the sources as you'd
like to use, and let it comb them all, looking for your settings.

This README is admittedly very light on details. Full documentation will come
in time. For now, here's an example of its use:

Import the library::

    import setoptconf as soc

Instantiate the manager::

    manager = soc.ConfigurationManager('myprogram')

Define the settings we'd like to collect::

    manager.add(soc.StringSetting('foo'))
    manager.add(soc.IntegerSetting('bar', required=True))
    manager.add(soc.BooleanSetting('baz', default=True))

Retreive the settings from our desired sources, combining the settings and
overriding with the priority implied by the order of the sources we pass::

    config = manager.retrieve(
        # This source pulls from the command line using argparse.
        soc.CommandLineSource,

        # This source pulls from environment variables that are prefixed
        # with MYPROGRAM_*
        soc.EnvironmentVariableSource,

        # This source pulls from the named INI files. It stops at the first
        # file it finds.
        soc.ConfigFileSource(('.myprogramrc', '/etc/myprogram.conf')),
    )

We now have a Configuration object named ``config`` that has three attributes;
``foo``, ``bar``, and ``baz``.

