# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import pytest

from mozbitbar import MozbitbarCredentialException
from mozbitbar.configuration import Configuration


@pytest.mark.parametrize('kwargs,expected', [
    (
        {
            'TESTDROID_USERNAME': 'MOCK_TEST',
            'TESTDROID_PASSWORD': 'MOCK_TEST',
            'TESTDROID_APIKEY': 'MOCK_TEST',
            'TESTDROID_URL': 'https://www.mock_test.com',
        },
        {
            'user_name': 'MOCK_TEST',
            'user_password': 'MOCK_TEST',
            'api_key': 'MOCK_TEST',
            'url': 'https://www.mock_test.com',
        }
    ),
    (
        {
            'TESTDROID_USERNAME': 'MOCK_TEST',
            'TESTDROID_PASSWORD': 'MOCK_TEST',
            'TESTDROID_URL': 'https://www.mock_test.com'
        },
        {
            'user_name': 'MOCK_TEST',
            'user_password': 'MOCK_TEST',
            'api_key': None,
            'url': 'https://www.mock_test.com',
        }
    ),
    (
        {
            'TESTDROID_USERNAME': 'MOCK_TEST'
        },
        MozbitbarCredentialException
    )
])
def test_configuration_from_kwargs(kwargs, expected):
    """Ensures the Configuration object can be instantiated with appropriate
    values provided to the constructor.
    """
    if expected is MozbitbarCredentialException:
        with pytest.raises(MozbitbarCredentialException):
            config = Configuration(**kwargs)
    else:
        config = Configuration(**kwargs)
        assert config.client is not None
        for attribute, value in expected.iteritems():
            assert hasattr(config, attribute)
            assert getattr(config, attribute) == value


@pytest.mark.parametrize('kwargs,expected', [
    (
        {
            'TESTDROID_USERNAME': 'MOCK_ENVIRONMENT_VALUE_TEST',
            'TESTDROID_PASSWORD': 'MOCK_ENVIRONMENT_VALUE_TEST',
            'TESTDROID_APIKEY': 'MOCK_ENVIRONMENT_VALUE_TEST',
            'TESTDROID_URL': 'https://www.mock_test_env_var.com',
        },
        {
            'user_name': 'MOCK_ENVIRONMENT_VALUE_TEST',
            'user_password': 'MOCK_ENVIRONMENT_VALUE_TEST',
            'api_key': 'MOCK_ENVIRONMENT_VALUE_TEST',
            'url': 'https://www.mock_test_env_var.com',
        }
    ),
    (
        {
            'TESTDROID_USERNAME': 'MOCK_ENVIRONMENT_VALUE_TEST',
            'TESTDROID_PASSWORD': 'MOCK_ENVIRONMENT_VALUE_TEST',
            'TESTDROID_URL': 'https://www.mock_test_env_var.com',
        },
        {
            'user_name': 'MOCK_ENVIRONMENT_VALUE_TEST',
            'user_password': 'MOCK_ENVIRONMENT_VALUE_TEST',
            'api_key': None,
            'url': 'https://www.mock_test_env_var.com',
        }
    ),
    (
        {
            'TESTDROID_APIKEY': 'MOCK_ENVIRONMENT_API_KEY',
            'TESTDROID_URL': 'https://www.mock_test_env_var.com',
        },
        {
            'api_key': 'MOCK_ENVIRONMENT_API_KEY',
            'url': 'https://www.mock_test_env_var.com',
        }
    ),
    (
        {
            'TESTDROID_URL': 'https://www.mock_test_env_var.com',
        },
        MozbitbarCredentialException
    )
])
def test_configuration_from_env_var(kwargs, expected, monkeypatch):
    """Ensures the Configuration object can be instantiated using
    key values set from environment variables.
    """
    # dynamically patch the environment variable under test.
    # first delete the environment variables.
    monkeypatch.delenv('TESTDROID_USERNAME')
    monkeypatch.delenv('TESTDROID_PASSWORD')
    monkeypatch.delenv('TESTDROID_APIKEY')
    monkeypatch.delenv('TESTDROID_URL')

    # then set only the variables that were provided by test data.
    for key, attribute in kwargs.iteritems():
        monkeypatch.setenv(key, attribute)

    if expected is MozbitbarCredentialException:
        with pytest.raises(MozbitbarCredentialException):
            config = Configuration()
    else:
        config = Configuration()
        assert config.client is not None
        for attribute, value in expected.iteritems():
            assert hasattr(config, attribute)
            assert getattr(config, attribute) == value
