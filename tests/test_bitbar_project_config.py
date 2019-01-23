# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import pytest

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


# Project config #


@pytest.mark.parametrize('kwargs,expected', [
    (
        {'timeout': 10},
        {'timeout': 10}
    ),
    (
        {'timeout': 10, 'scheduler': 'SINGLE'},
        {'timeout': 10, 'scheduler': 'SINGLE'}
    ),
    pytest.param(
        'not_a_dict',
        TypeError,
        marks=pytest.mark.xfail
    ),
    (
        {'scheduler': 'SINGLE'},
        None
    ),
])
def test_set_project_config_new_config(initialize_project, kwargs, expected):
    if expected == TypeError:
        with pytest.raises(TypeError):
            initialize_project.set_project_configs(new_values=kwargs)
    else:
        initialize_project.set_project_configs(new_values=kwargs)


@pytest.mark.parametrize('mock_path,kwargs,expected', [
    (
        '10',
        {'content': 10},
        {'content': 10}
    ),
])
def test_set_project_config_path(write_tmp_file, initialize_project, mock_path,
                                 kwargs, expected):
    path = write_tmp_file(kwargs, fmt='json', file_path=mock_path)

    assert (
        initialize_project.set_project_configs(path=path.strpath) is None)


@pytest.mark.parametrize('mock_path,kwargs,expected', [
    (
        'mock_file.json',
        {'mock': True},
        {'mock': True}
    ),
    (
        'valid_mock_path.json',
        {"scheduler": "SINGLE", "timeout": 0},
        {"scheduler": "SINGLE", "timeout": 0}
    ),
    (
        'mock_path',
        -1,
        TypeError
    )
])
def test_load_project_config(write_tmp_file, initialize_project, mock_path,
                             kwargs, expected):
    path = write_tmp_file(kwargs, fmt='json', file_path=mock_path)

    if expected == TypeError:
        with pytest.raises(TypeError):
            initialize_project._load_project_config(path.strpath)

    else:
        assert expected == initialize_project._load_project_config(
                                                    path.strpath)
