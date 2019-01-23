# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import pytest

from mozbitbar import MozbitbarFrameworkException
from mozbitbar.bitbar_project import BitbarProject


@pytest.fixture
def initialize_project():
    # initialize a dummy project for when the __init__ method is not
    # under test.
    kwargs = {
        'project_name': 'mock_project',
        'TESTDROID_USERNAME': 'MOCK_ENVIRONMENT_VALUE_TEST',
        'TESTDROID_PASSWORD': 'MOCK_ENVIRONMENT_VALUE_TEST',
        'TESTDROID_APIKEY': 'MOCK_ENVIRONMENT_VALUE_TEST',
        'TESTDROID_URL': 'https://www.mock_test_env_var.com',
    }
    return BitbarProject('existing', **kwargs)


@pytest.mark.parametrize('kwargs,expected', [
    (
        {'framework': -1},
        MozbitbarFrameworkException
    ),
    (
        {'framework': 'should_not_match_anything'},
        MozbitbarFrameworkException
    ),
    (
        {'framework': 1},
        {'framework_name': 'mock_framework', 'framework_id': 1}
    ),
    (
        {'framework': 'mock_framework'},
        {'framework_name': 'mock_framework', 'framework_id': 1}
    ),
    (
        {'framework': u'mock_framework'},
        {'framework_name': 'mock_framework', 'framework_id': 1}
    ),
    (
        {'framework': 'mock_unicode_framework'},
        {'framework_name': 'mock_unicode_framework', 'framework_id': 2}
    )
])
def test_bb_project_framework(initialize_project, kwargs, expected):
    if expected is MozbitbarFrameworkException:
        with pytest.raises(MozbitbarFrameworkException):
            initialize_project.set_project_framework(**kwargs)
    else:
        initialize_project.set_project_framework(**kwargs)
        assert initialize_project.framework_id == expected['framework_id']
        assert initialize_project.framework_name == expected['framework_name']
