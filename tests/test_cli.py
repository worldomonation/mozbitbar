# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import pytest

from mozbitbar.cli import parse_arguments, cli


@pytest.mark.parametrize('kwargs,expected', [
    (
        ['-r', '/mock_recipe/'],
        {'recipe': '/mock_recipe/'}
    ),
    (
        ['-r', 'mock_recipe', 'discard'],
        {'recipe': 'mock_recipe'}
    ),
    (
        ['--recipe', 'mock_recipe', '-v'],
        {'recipe': 'mock_recipe', 'verbose': True}
    ),
    (
        ['-q'],
        {'quiet': True}
    )
])
def test_parse_arguments(kwargs, expected):
    args, _ = parse_arguments(kwargs)

    assert args
    for key, value in expected.iteritems():
        assert getattr(args, key) == value


@pytest.mark.parametrize('kwargs,expected', [
    (
        ['python', '-r', 'mock_recipe'],
        {'recipe': 'mock_recipe'}
    )
])
def test_cli(kwargs, expected):
    args = cli(kwargs)

    assert args
    for key, value in expected.iteritems():
            assert getattr(args, key) == value
