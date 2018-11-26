from __future__ import print_function, absolute_import

import pytest
import testdroid

from mock import patch


@pytest.fixture(autouse=True)
def mock_testdroid_client(monkeypatch):
    with patch.object(testdroid.Testdroid, '__init__') as client:
        client.username = 'test_username'
        client.url = 'https://testingurl.com'
        client.password = 'test_password'
        client.apikey = 'test_apikey'
        return client