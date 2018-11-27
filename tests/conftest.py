from __future__ import print_function, absolute_import

import pytest


from testdroid import Testdroid
from mozbitbar.bitbar_project import BitbarProject

from mock import patch


@pytest.fixture(autouse=True)
def mock_testdroid_client(monkeypatch):
    def init():
        with patch.object(Testdroid, '__init__') as client:
            client.username = 'test_username'
            client.url = 'https://testingurl.com'
            client.password = 'test_password'
            client.apikey = 'test_apikey'
            return client

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

    monkeypatch.setattr(Testdroid, 'get_token', get_token_wrapper)
    monkeypatch.setattr(Testdroid, 'get_project', get_project_wrapper)

    return init


@pytest.fixture(autouse=True)
def mock_bitbar_project(monkeypatch):
    def init(project_status, **kwargs):
        with patch.object(BitbarProject, '__init__') as project:
            project.project_id = kwargs.get('project_id')
            project.name = 'mock_project'
            project.type = 'mock_type'
            project.framework_id = 99
            project.device_group_id = 1
            return project

    return init
