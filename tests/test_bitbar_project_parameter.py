# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import pytest

from mozbitbar import MozbitbarProjectException
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


@pytest.mark.parametrize('parameter,overwrite,expected', [
    (
        {},
        False,
        None
    ),
    (
        [{'key': 'test_key', 'value': 'test_value'}],
        False,
        None
    ),
    (
        [{'key': 'mock_project_parameter_1', 'value': 'unique_value'}],
        False,
        None
    ),
    (
        [{'key': 'unacceptable_key', 'value': 'unacceptable_value'}],
        False,
        MozbitbarProjectException
    ),
    (
        [{'key': 'mock_project_parameter_1', 'value': 'modified_value'}],
        True,
        None
    )
])
def test_set_project_parameters(initialize_project, parameter, overwrite,
                                expected):
    if expected == MozbitbarProjectException:
        with pytest.raises(MozbitbarProjectException):
            initialize_project.set_project_parameters(parameter, overwrite)
    else:
        assert expected == initialize_project.set_project_parameters(parameter,
                                                                     overwrite)


@pytest.mark.parametrize('parameter,expected', [
    (
        'mock_project_parameter_1',
        None
    ),
    (
        '319',
        None
    ),
    (
        321,
        None
    ),
    (
        'does_not_exist',
        None
    )
])
def test_delete_project_parameters(initialize_project, parameter, expected):
    if expected == MozbitbarProjectException:
        with pytest.raises(MozbitbarProjectException):
            initialize_project.delete_project_parameter(parameter)
    else:
        assert expected == initialize_project.delete_project_parameter(
                                parameter)
