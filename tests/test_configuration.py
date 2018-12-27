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
def test_configuration(kwargs,expected):
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
