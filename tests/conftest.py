from __future__ import print_function, absolute_import

import random

import pytest


from testdroid import Testdroid
from mozbitbar.bitbar_project import BitbarProject

from mock import patch


@pytest.fixture(autouse=True)
def mock_testdroid_client(monkeypatch):
    def init(object, **kwargs):
        with patch.object(Testdroid, '__init__') as client:
            client.apikey = 'test_apikey'
            client.username = 'test_username'
            client.password = 'test_password'
            client.cloud_url = 'https://testingurl.com'
            client.download_buffer_size = 65536

    def create_project_wrapper(object, project_name, project_type):
        return {
            'id': random.randint(1, 10),
            'name': project_name,
            'type': project_type
        }

    def get_me_wrapper(object):
        return '{}'

    def get_token_wrapper(object):
        return 'test_access_token'

    def get_project_wrapper(object, project_id):
        return {
            'id': project_id,
            'name': 'mock_project',
            'type': 'mock_type',
            'osType': 'mock_type',
            'frameworkId': 99
        }

    def get_projects_wrapper(object):
        return {
            'data': [
                {
                    'id': 1,
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

    monkeypatch.setattr(Testdroid, '__init__', init)
    monkeypatch.setattr(Testdroid, 'create_project', create_project_wrapper)
    monkeypatch.setattr(Testdroid, 'get_me', get_me_wrapper)
    monkeypatch.setattr(Testdroid, 'get_token', get_token_wrapper)
    monkeypatch.setattr(Testdroid, 'get_project', get_project_wrapper)
    monkeypatch.setattr(Testdroid, 'get_projects', get_projects_wrapper)

    import datetime
    datetime.datetime.second

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
