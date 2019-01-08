# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import random

import pytest
from requests import Response

from testdroid import Testdroid


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
        ]
    }


def mock_project_template(project_id=None, project_name=None,
                          project_type=None, project_framework_id=None):
    return {
        'id': project_id or random.randint(11, 20),
        'name': project_name or 'mock_project',
        'type': project_type or 'mock_type',
        'osType': 'mock_type',
        'frameworkId': 99 or project_framework_id,
    }


def mock_project_config(project_status=None, project_framework_id=None,
                        project_id=None, scheduler=None, **kwargs):
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
    if not kwargs:
        return base
    else:
        return dict(base.items() + kwargs.items())


@pytest.fixture(autouse=True)
def mock_testdroid_client(monkeypatch):

    def init_wrapper(object, **kwargs):
        object.username = kwargs.get('username')
        object.password = kwargs.get('password')
        object.api_key = kwargs.get('apikey')
        object.cloud_url = kwargs.get('url')

    # Project related mocks #

    def create_project_wrapper(object, project_name, project_type):
        return mock_project_template(project_name=project_name,
                                     project_type=project_type)

    def get_project_wrapper(object, project_id):
        # returns a single project, don't mistake with projects!
        return mock_project_template(project_id=project_id)

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

    # Device related mocks #

    def get_device_groups_wrapper(object):
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

    def get_devices_wrapper(object):
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
    monkeypatch.setattr(Testdroid, 'get_frameworks',
                        get_frameworks_wrapper)
    monkeypatch.setattr(Testdroid, 'get_input_files', get_input_files_wrapper)
    monkeypatch.setattr(Testdroid, 'get_devices', get_devices_wrapper)
    monkeypatch.setattr(Testdroid, 'get_device_groups',
                        get_device_groups_wrapper)
    monkeypatch.setattr(Testdroid, 'get_me', get_me_wrapper)
    monkeypatch.setattr(Testdroid, 'get_project', get_project_wrapper)
    monkeypatch.setattr(Testdroid, 'get_projects', get_projects_wrapper)
    monkeypatch.setattr(
        Testdroid, 'get_project_config', get_project_config_wrapper)
    monkeypatch.setattr(Testdroid, 'get_token', get_token_wrapper)
    monkeypatch.setattr(Testdroid, 'set_project_config',
                        set_project_config_wrapper)
    monkeypatch.setattr(Testdroid, 'set_project_framework',
                        set_project_framework_wrapper)
    monkeypatch.setattr(Testdroid, 'upload', upload_wrapper)
