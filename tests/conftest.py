# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import random

import pytest
from requests import Response

from testdroid import RequestResponseError, Testdroid


def mock_projects_list():
    return {
        'data': [
            {
                'id': 11,
                'name': 'mock_project',
                'type': 'mock_type',
                'osType': 'mock_type',
                'frameworkId': 99
            },
            {
                'id': 99,
                'name': 'another_mock_project',
                'type': 'second_mock_type',
                'osType': 'second_mock_type',
                'frameworkId': 88
            },
            {
                'id': 10000,
                'name': 'yet_another_mock_project',
                'type': 'third_mock_type',
                'osType': 'third_mock_type',
                'frameworkId': 12345
            },
            {
                'id': 99999,
                'name': u'mock_project_4',
                'type': u'fourth_mock_type',
                'osType': u'fourth_mock_type',
                'frameworkId': 12345
            },
        ]
    }


def mock_device_groups_list():
    return {
        'data': [
            {
                'displayName': 'mock_device_group',
                'userId': 8080,
                'deviceCount': 20,
                'osType': 'mock_os',
                'id': 7070
            },
            {
                'displayName': 'second_mock_group',
                'userId': 8080,
                'deviceCount': 10,
                'osType': 'different_mock_os',
                'id': 7171
            }
        ]
    }


def mock_devices_list():
    return {
        'data': [
            {
                'displayName': 'mock_device_1',
                'osType': 'mock_os',
                'id': 707,
            },
            {
                'displayName': 'mock_device_2',
                'osType': 'mock_os',
                'id': 717,
            },
            {
                'displayName': 'mock_device_3',
                'osType': 'mock_os',
                'id': 727,
            },
        ]
    }


def mock_project_config(project_status=None, project_framework_id=None,
                        project_id=None, scheduler=None, **kwargs):
    """This method allows the mock method to dynamically build the project
    configuration that is desired, by passing in values where desired.
    """
    base = {
        'status': project_status or None,
        'frameworkId': project_framework_id or None,
        'projectId': project_id or random.randint(11, 20),
        'testRunParameters': [
            {
                "value": "mock_config_value",
                "selfURI": 'null',
                "id": random.randint(1053092600, 1053092700),
                "key": "mock_config_key"
            }
        ],
        'scheduler': scheduler or 'PARALLEL'
    }
    # kwargs is to handle values that do not exist in the `base` dictionary,
    # simulating scenario where user calls Testdroid to set a previously unset
    # project configuration value.
    if not kwargs:
        return base
    else:
        return dict(base.items() + kwargs.items())


def mock_project_parameters(parameter=None):
    base = [
        {
            'key': 'mock_project_parameter_1',
            'value': 'mock_value_1',
            'id': 319
        },
        {
            'key': 'mock_project_parameter_2',
            'value': 'mock_value_2',
            'id': 320
        },
        {
            'key': 'mock_project_parameter_3',
            'value': 'mock_value_3',
            'id': 321
        }
    ]
    if not parameter:
        return base
    else:
        if parameter.get('key') == 'unacceptable_key':
            raise RequestResponseError(msg='mock', status_code=400)
        if any(parameter.get('key') in item.get('key') for item in base):
            raise RequestResponseError(msg='mock', status_code=409)
        else:
            parameter['id'] = 330
            base.append(parameter)
            return parameter


def mock_test_runs():
    return {
        'data': [
            {
                'number': 8,
                'id': 757,
                'displayName': 'mock_test_run_1'
            },
            {
                'number': 9,
                'id': 767,
                'displayName': 'mock_test_run_2'
            },
            {
                'number': 10,
                'id': 777,
                'displayName': 'mock_test_run_3'
            },
        ]
    }


@pytest.fixture(autouse=True)
def mock_testdroid_client(monkeypatch):
    """Mocks essentially all of the Testdroid methods used by Mozbitbar.

    These mocked methods are meant to replace the Testdroid calls to the live
    API when running tests.
    """
    def init_wrapper(object, **kwargs):
        object.username = kwargs.get('username')
        object.password = kwargs.get('password')
        object.api_key = kwargs.get('apikey')
        object.cloud_url = kwargs.get('url')

    # Project related mocks #

    def create_project_wrapper(object, project_name, project_type):
        return {
            'id': random.randint(100, 200),
            'name': project_name or 'mock_project',
            'type': project_type or 'mock_type',
            'osType': 'mock_type',
            'frameworkId': 99,
        }

    def get_projects_wrapper(object):
        return mock_projects_list()

    def set_project_framework_wrapper(object, project_id, framework_id):
        # not a stub - Testdroid method does not return anything.
        pass

    # Framework related mocks #

    def get_frameworks_wrapper(object):
        return {
            'data': [
                {
                    'id': 1,
                    'name': 'mock_framework'
                },
                {
                    'id': 100,
                    'name': 'another_mock_framework'
                },
                {
                    'id': 2,
                    'name': u'mock_unicode_framework'
                }
            ]
        }

    # File related mocks #

    def get_input_files_wrapper(object):
        return {
            'data': [
                {
                    'name': 'mock_file.zip'
                },
                {
                    'name': 'mocked_application_file.apk'
                },
                {
                    'name': u'mocked_unicode_file.apk'
                }
            ]
        }

    def upload_wrapper(object, path, filename):
        res = Response()
        res.status_code = 200
        return res

    # Config related mocks #

    def get_project_config_wrapper(object, project_id):
        return mock_project_config(project_id)

    def set_project_config_wrapper(object, project_id, **kwargs):
        return mock_project_config(**kwargs)

    # Parameter related mocks #

    def set_project_parameters_wrapper(object, project_id, parameters):
        return mock_project_parameters(parameters)

    def delete_project_parameters_wrapper(object, project_id, parameter_id):
        parameters = mock_project_parameters()
        for item in parameters:
            if item.get('id') == parameter_id:
                res = Response()
                res.status_code = 204
                return res
        raise RequestResponseError(msg='mock', status_code=404)

    def get_project_parameters_wrapper(object, project_id):
        return {
            'data': mock_project_parameters()
        }

    # Device related mocks #

    def get_device_groups_wrapper(object):
        return mock_device_groups_list()

    def get_devices_wrapper(object):
        return mock_devices_list()

    # Test Run mocks #

    def get_project_test_runs_wrapper(object, project_id):
        return mock_test_runs()

    def get_test_run_wrapper(object, project_id, test_run_id):
        if type(test_run_id) is not int:
            raise RequestResponseError(msg='', status_code=400)
        output = mock_test_runs()['data']
        for item in output:
            if item['id'] == test_run_id:
                return item
        raise RequestResponseError(msg='mock', status_code=404)

    def start_test_run_wrapper(object, project_id, device_group_id=None,
                               device_model_ids=None, name=None,
                               additional_params={}):
        if not device_group_id and not device_model_ids:
            return
        else:
            return 220

    # Additional mocks #

    def get_me_wrapper(object):
        return {
            'id': 1,
            'accountId': 2,
            'name': 'Mock User',
        }

    def get_token_wrapper(object):
        return 'test_access_token'

    # Monkeypatch #

    monkeypatch.setattr(Testdroid, '__init__', init_wrapper)
    monkeypatch.setattr(Testdroid, 'create_project', create_project_wrapper)
    monkeypatch.setattr(Testdroid, 'delete_project_parameters',
                        delete_project_parameters_wrapper)
    monkeypatch.setattr(Testdroid, 'get_project_test_runs',
                        get_project_test_runs_wrapper)
    monkeypatch.setattr(Testdroid, 'get_frameworks',
                        get_frameworks_wrapper)
    monkeypatch.setattr(Testdroid, 'get_input_files', get_input_files_wrapper)
    monkeypatch.setattr(Testdroid, 'get_devices', get_devices_wrapper)
    monkeypatch.setattr(Testdroid, 'get_device_groups',
                        get_device_groups_wrapper)
    monkeypatch.setattr(Testdroid, 'get_me', get_me_wrapper)
    monkeypatch.setattr(Testdroid, 'get_projects', get_projects_wrapper)
    monkeypatch.setattr(
        Testdroid, 'get_project_config', get_project_config_wrapper)
    monkeypatch.setattr(
        Testdroid, 'get_project_parameters', get_project_parameters_wrapper)
    monkeypatch.setattr(Testdroid, 'get_token', get_token_wrapper)
    monkeypatch.setattr(Testdroid, 'get_test_run', get_test_run_wrapper)
    monkeypatch.setattr(Testdroid, 'set_project_config',
                        set_project_config_wrapper)
    monkeypatch.setattr(Testdroid, 'set_project_framework',
                        set_project_framework_wrapper)
    monkeypatch.setattr(Testdroid, 'set_project_parameters',
                        set_project_parameters_wrapper)
    monkeypatch.setattr(Testdroid, 'start_test_run', start_test_run_wrapper)
    monkeypatch.setattr(Testdroid, 'upload', upload_wrapper)
