from __future__ import print_function, absolute_import

import random

import pytest


from testdroid import Testdroid
from mozbitbar.bitbar_project import BitbarProject

from mock import patch


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
        'id': project_id or random.randint(1, 10),
        'name': project_name or 'mock_project',
        'type': project_type or 'mock_type',
        'osType': 'mock_type',
        'frameworkId': 99 or project_framework_id
    }


@pytest.fixture(autouse=True)
def mock_testdroid_client(monkeypatch):
    def init(object, **kwargs):
        with patch.object(Testdroid, '__init__') as client:
            client.apikey = 'test_apikey'
            client.username = 'test_username'
            client.password = 'test_password'
            client.cloud_url = 'https://testingurl.com'
            client.download_buffer_size = 65536

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

    def upload_file_wrapper(object, path, filename):
        pass
        # TODO: stub mock wrapper

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

    monkeypatch.setattr(Testdroid, '__init__', init)
    monkeypatch.setattr(Testdroid, 'create_project', create_project_wrapper)
    monkeypatch.setattr(Testdroid, 'get_frameworks',
                        get_frameworks_wrapper)
    monkeypatch.setattr(Testdroid, 'get_input_files', get_input_files_wrapper)
    monkeypatch.setattr(Testdroid, 'get_me', get_me_wrapper)
    monkeypatch.setattr(Testdroid, 'get_token', get_token_wrapper)
    monkeypatch.setattr(Testdroid, 'get_project', get_project_wrapper)
    monkeypatch.setattr(Testdroid, 'get_projects', get_projects_wrapper)
    monkeypatch.setattr(Testdroid, 'set_project_framework',
                        set_project_framework_wrapper)
    monkeypatch.setattr(Testdroid, 'upload_file', upload_file_wrapper)

    return init


@pytest.fixture(autouse=True)
def mock_bitbar_project(monkeypatch):
    def init(project_status, **kwargs):
        with patch.object(BitbarProject, '__init__') as project:
            project.project_id = kwargs.get('id') or 1
            project.name = kwargs.get('name') or 'mock_type'
            project.type = 'mock_type'
            project.framework_id = 99
            project.device_group_id = 1
            return project

    return init
