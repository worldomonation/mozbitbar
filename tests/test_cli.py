# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import pytest

import mozbitbar.cli as cli
from mozbitbar import MozbitbarRecipeException


@pytest.mark.parametrize('kwargs,expected', [
    (
        ['python', '-r', 'mock_recipe'],
        {'recipe': 'mock_recipe'}
    ),
    (
        ['-r', '/absolute_path_mock_recipe/'],
        {'recipe': '/absolute_path_mock_recipe/'}
    ),
    (
        ['-r', 'kept_option', 'discarded_option'],
        {'recipe': 'kept_option'}
    ),
    (
        ['--recipe', 'verbose_recipe', '-v'],
        {'recipe': 'verbose_recipe', 'verbose': True}
    ),
    (
        ['-q'],
        MozbitbarRecipeException
    ),
    (
        ['-v'],
        MozbitbarRecipeException
    ),
    (
        ['-r', 'mock_recipe_file', '-c', 'temp_file.yaml'],
        {'credentials': 'temp_file.yaml', 'recipe': 'mock_recipe_file'}
    )
])
def test_cli(kwargs, expected):
    if type(expected) == type:
        with pytest.raises(expected):
            args = cli.cli(kwargs)
    else:
        args = cli.cli(kwargs)

        assert args
        for key, value in expected.iteritems():
                assert getattr(args, key) == value


@pytest.mark.parametrize('parser_options', [
    (
        '-r', '-v', '-q', '-c'
    ),
    (
        '--recipe', '--verbose', '--quiet', '--credentials'
    )
])
def test_get_parser(parser_options):
    parser = cli.get_parser()
    for option in parser_options:
        assert option in parser._option_string_actions.keys()
