import os.path
import re
import sys

from setuptools import setup, find_packages


PYVER = sys.version_info
SETUP_KWARGS = {}
DEPENDENCIES = []


# Do we need to install argparse?
if PYVER < (2, 7):
    DEPENDENCIES.append('argparse')
elif PYVER >= (3, 0) and PYVER < (3, 2):
    DEPENDENCIES.append('argparse')


# Are we on Py3K?
if PYVER >= (3, 0):
    SETUP_KWARGS['use_2to3'] = True


def get_version():
    init = os.path.join(os.path.dirname(__file__), 'setoptconf/__init__.py')
    source = open(init, 'r').read()
    version = re.search(
        r"__version__ = '(?P<version>[^']+)'",
        source,
    ).group('version')
    return version


def get_description():
    readme = os.path.join(os.path.dirname(__file__), 'README.rst')
    return open(readme, 'r').read()


setup(
    name='setoptconf',
    version=get_version(),
    author='Jason Simeone',
    author_email='jay@classless.net',
    license='MIT',
    keywords=['settings', 'options', 'configuration', 'config', 'arguments'],
    description='A module for retrieving program settings from various'
                ' sources in a consistant method.',
    long_description=get_description(),
    url='https://github.com/jayclassless/setoptconf',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(exclude=['test.*', 'test']),
    install_requires=DEPENDENCIES,
    extras_require={
        'YAML': ['pyyaml'],
    },
    **SETUP_KWARGS
)
