# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import pytest

from mozbitbar import (
    MozbitbarBaseException,
    MozbitbarFileException
)

@pytest.mark.parametrize('kwargs,expected', [
    (
        {
            'message': 'mock_test',
            'status_code': 200
        },
        {
            'message': 'mock_test',
            'status_code': 200
        }
    ),
    (
        {
            'message': 'mock_test'
        },
        {
            'message': 'mock_test'
        }
    )
])
def test_base_exception(kwargs, expected):
    e = MozbitbarBaseException(**kwargs)
    assert e.message == expected.get('message')
    assert e.status_code == expected.get('status_code')


@pytest.mark.parametrize('kwargs,expected', [
    (
        {
            'message': 'mock_file_exception_test',
            'status_code': 300,
            'path': '/mock/path'
        },
        {
            'message': 'mock_file_exception_test',
            'status_code': 300,
            'path': '/mock/path'
        },
    )
])
def test_file_exception(kwargs, expected):
    e = MozbitbarFileException(**kwargs)
    assert e.message == expected.get('message')
    assert e.status_code == expected.get('status_code')
    assert e.path == expected.get('path')
