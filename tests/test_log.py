# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import logging

import pytest

from mozbitbar import log


@pytest.mark.parametrize('kwargs,expected', [
    (
        {},
        {
            'level': logging.INFO,
            'name': 'mozbitbar',
            'fmt': log._default_fmt
        }
    ),
    (
        {
            'verbose': True,
            'name': 'mock_logger'
        },
        {
            'level': logging.DEBUG,
            'name': 'mock_logger',
            'fmt': log._default_fmt
        },
    ),
    (
        {
            'quiet': True,
            'fmt': '%(thread)d'
        },
        {
            'name': 'mozbitbar',
            'level': logging.WARNING,
            'fmt': '%(thread)d',
        },
    ),
])
def test_setup_logger(kwargs, expected):
    logger = log.setup_logger(**kwargs)
    assert logger.propagate is False
    assert logger.level is expected['level']
    assert logger.name == expected['name']
    assert logger.handlers[0].formatter._fmt == expected['fmt']
