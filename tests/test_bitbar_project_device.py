# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import pytest

from mozbitbar import MozbitbarDeviceException
from mozbitbar.bitbar_project import BitbarProject


@pytest.fixture()
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
        {'device_group_id': 7070},
        {'device_group_id': 7070, 'device_group_name': 'mock_device_group'}
    ),
    (
        {},
        MozbitbarDeviceException
    ),
    (
        {'device_group_name': 'mock_device_group'},
        {'device_group_name': 'mock_device_group', 'device_group_id': 7070}
    ),
    (
        {'device_group_name': 'no_group', 'device_group_id': -1},
        MozbitbarDeviceException
    ),
    (
        {'device_group_name': 'second_mock_group'},
        {'device_group_name': 'second_mock_group', 'device_group_id': 7171},
    )
])
def test_set_device_group(initialize_project, kwargs, expected):
    if expected == MozbitbarDeviceException:
        with pytest.raises(expected):
            initialize_project.set_device_group(**kwargs)
    else:
        initialize_project.set_device_group(**kwargs)
        initialize_project.device_group_id = expected.get('device_group_id')
        initialize_project.device_group_name = expected.get(
                                                    'device_group_name')


@pytest.mark.parametrize('kwargs,expected', [
    (
        {'device_id': 707},
        {'device_id': 707, 'device_name': 'mock_device_1'}
    ),
    (
        {},
        MozbitbarDeviceException
    ),
    (
        {'device_name': 'mock_device_2'},
        {'device_name': 'mock_device_group', 'device_id': 717}
    ),
    (
        {'device_name': 'no_group', 'device_id': -1},
        MozbitbarDeviceException
    ),
    (
        {'device_name': 'mock_device_3'},
        {'device_name': 'mock_device_3', 'device_group_id': 727},
    )
])
def test_set_device(initialize_project, kwargs, expected):
    if expected == MozbitbarDeviceException:
        with pytest.raises(expected):
            initialize_project.set_device(**kwargs)
    else:
        initialize_project.set_device(**kwargs)
        initialize_project.device_d = expected.get('device_group_id')
        initialize_project.device_name = expected.get('device_group_name')


@pytest.mark.parametrize('device_id,expected', [
    (1, 1),
    ('1', 1),
    (-1, -1),
    ({}, TypeError),
    ([], TypeError)
])
def test_device_id(initialize_project, device_id, expected):
    if expected == TypeError:
        with pytest.raises(expected):
            initialize_project.device_id = device_id
    else:
        initialize_project.device_id = device_id
        assert initialize_project.device_id == expected


@pytest.mark.parametrize('device_group_id,expected', [
    (1, 1),
    ('1', 1),
    (-1, -1),
    ({}, TypeError)
])
def test_device_group_id(initialize_project, device_group_id, expected):
    if expected == TypeError:
        with pytest.raises(expected):
            initialize_project.device_group_id = device_group_id
    else:
        initialize_project.device_group_id = device_group_id
        assert initialize_project.device_group_id == expected


@pytest.mark.parametrize('device_group_name,expected', [
    (1, '1'),
    (-1, '-1'),
    ({}, '{}'),
    ('string', 'string')
])
def test_device_group_name(initialize_project, device_group_name, expected):
    if expected == TypeError:
        with pytest.raises(expected):
            initialize_project.device_group_name = device_group_name
    else:
        initialize_project.device_group_name = device_group_name
        assert initialize_project.device_group_name == expected
