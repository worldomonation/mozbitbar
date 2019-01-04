# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import mock
import os
import random

import pytest
import yaml

from mozbitbar import MozbitbarRecipeException
from mozbitbar.recipe_handler import Recipe


def generate_recipe():
    recipe = {
        'project': random.choice(['existing', 'new']),
        'arguments': {

        }
    }


@pytest.fixture(autouse=True)
def mock_recipe():
    with mock.patch.object(Recipe, '__init__', return_value=None):
        recipe_obj = Recipe('')
        return recipe_obj


@pytest.mark.parametrize('kwargs', [
    ({
        'file_name': 'mock_parametrized_recipe.yaml'
    }),
    ({
        'file_name': 'another_mock_file.yaml',
        'content': 'dummy'
    })
])
def test_locate_recipe(tmpdir, mock_recipe, kwargs):
    mock_file_name = kwargs.get('file_name' or 'mock_recipe.yaml')
    path = tmpdir.mkdir('mock').join(mock_file_name)

    content = kwargs.get('content') or {'project': 'existing',
                                        'arguments': {
                                            'project_id': 10101010,
                                            'project_name': 'mock_project'}
                                       }
    yaml_converted_content = yaml.dump(content)
    path.write(yaml_converted_content)

    mock_recipe.locate_recipe(path.strpath)
    assert mock_recipe.recipe_path == path.strpath
    assert mock_recipe.recipe_name == path.basename


@pytest.mark.parametrize('kwargs,expected', [
    (
        [{
            'project': 'existing',
            'arguments': {
                'project_id': 1
            }
        }],
        None.__class__
    ),
    (
        [{
            'project': 'mock',
            'arguments': {}
        }],
        MozbitbarRecipeException
    ),
    (
        [{
            'project': 'mock'
        }],
        TypeError
    ),
    (
        [{
            'project': 'mock',
            'arguments': []
        }],
        TypeError
    ),
    (
        [{
            'project': 'mock',
            'arguments': {}
        }],
        MozbitbarRecipeException
    ),
    (
        [{
            'arguments': {}
        }],
        MozbitbarRecipeException
    ),
])
def test_validate_recipe(tmpdir, mock_recipe, kwargs, expected):
    if issubclass(expected, Exception):
        with pytest.raises(expected):
            mock_recipe.validate_recipe(kwargs)
    else:
        mock_recipe.validate_recipe(kwargs)
        assert mock_recipe.project_arguments is not None
