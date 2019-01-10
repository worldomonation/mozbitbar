# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import pytest

from mozbitbar.bitbar_project import BitbarProject
from mozbitbar import MozbitbarTestRunException


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


@pytest.mark.parametrize('name,expected', [
    (
        'mock_test_run_1',
        False
    ),
    (
        'mock_test_run_0',
        True
    ),
    (
        None,
        None
    ),
    (
        1,
        True
    ),
    (
        ['mock_test_run_1'],
        True
    )
])
def test_is_test_name_unique(initialize_project, name, expected):
    assert expected == initialize_project._is_test_name_unique(name)


@pytest.mark.parametrize('kwargs,expected', [
    (
        {'test_run_id': 757},
        {
            'number': 8,
            'id': 757,
            'displayName': 'mock_test_run_1'
        },
    ),
    (
        {'test_run_name': 'mock_test_run_3'},
        {
            'number': 10,
            'id': 777,
            'displayName': 'mock_test_run_3'
        },
    ),
    (
        {'test_run_id': -1},
        MozbitbarTestRunException
    )
])
def test_get_test_run(initialize_project, kwargs, expected):
    if expected == MozbitbarTestRunException:
        with pytest.raises(expected) as exc:
            initialize_project.get_test_run(**kwargs)
        assert exc.value.status_code in [404, 400]
    else:
        assert expected == initialize_project.get_test_run(**kwargs)
