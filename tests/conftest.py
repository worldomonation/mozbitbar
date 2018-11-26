from __future__ import print_function, absolute_import

import pytest
import testdroid

from mock import patch


@pytest.fixture(autouse=True)
def mock_testdroid_client(monkeypatch):
    def init():
        with patch.object(testdroid.Testdroid, '__init__') as client:
            client.username = 'test_username'
            client.url = 'https://testingurl.com'
            client.password = 'test_password'
            client.apikey = 'test_apikey'
            return client

    def testdroid_get_token_wrapper(object):
        return 'test_access_token'

    def testdroid_get_project_wrapper(object, project_id):
        return {
            'id': project_id,
            'name': 'mock_project',
            'type': 'mock_type',
            'osType': 'mock_type',
            'frameworkId': 99
        }

    monkeypatch.setattr(testdroid.Testdroid, 'get_token', testdroid_get_token_wrapper)
    monkeypatch.setattr(testdroid.Testdroid, 'get_project',
                        testdroid_get_project_wrapper)

    return init
