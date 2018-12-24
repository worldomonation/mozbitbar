# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import pytest

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
            None
        }
    )
])
def test_configuration(kwargs, expected):
    """
    """
    config = Configuration(**kwargs)
    assert config.client is not None
    assert config.url is kwargs.get('TESTDROID_URL')
