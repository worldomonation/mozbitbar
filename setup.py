# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import os

from setuptools import setup

MAJOR_VERSION = 0
MINOR_VERSION = 0
REVISION = 1

PACKAGE_VERSION = '.'.join([
    str(item) for item in [MAJOR_VERSION, MINOR_VERSION, REVISION]
])
DESCRIPTION = '''Tool to interact with Bitbar REST API.'''
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')) as f:
    README = f.read()

DEPENDENCIES = [
    'pytest'
    'pyyaml',
    'testdroid',
]

setup(
    name='mozbitbar',
    version=PACKAGE_VERSION,
    description=DESCRIPTION,
    long_description=README,
    keywords='mozilla',
    author='Edwin Gao',
    author_email='egao@mozilla.com',
    url='https://github.com/worldomonation/mozbitbar',
    license='MPL',
    packages=['mozbitbar'],
    include_package_data=True,
    install_requires=DEPENDENCIES,
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    mozbitbar = mozbitbar.main:main
    """,
)
