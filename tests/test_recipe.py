# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import mock

import pytest
import yaml

from mozbitbar import MozbitbarRecipeException
from mozbitbar.recipe import Recipe


_default_recipe = {
    'project': 'existing',
    'arguments': {
        'project_id': 10101010,
        'project_name': 'mock_project'
    }
}


@pytest.fixture(autouse=True)
def mock_recipe():
    with mock.patch.object(Recipe, '__init__', return_value=None):
        recipe_obj = Recipe('')
        return recipe_obj


@pytest.mark.parametrize('kwargs,expected', [
    (
        {
            'file_name': 'mock_parametrized_recipe.yaml'
        },
        None.__class__
    ),
    (
        {
            'file_name': 'another_mock_file.yaml',
            'content': 'dummy'
        },
        None.__class__
    ),
    (
        {
            'file_name': 'mock_recipe_that_does_not_exist.yaml'
        },
        MozbitbarRecipeException
    ),
])
def test_locate_recipe(tmpdir, mock_recipe, kwargs, expected):
    if issubclass(expected, Exception):
        with pytest.raises(expected) as mre:
            mock_recipe.locate_recipe(kwargs.get('file_name'))
        assert 'recipe not found' in mre.value.message
    else:
        mock_file_name = kwargs.get('file_name') or 'mock_recipe.yaml'
        path = tmpdir.mkdir('mock').join(mock_file_name)

        content = kwargs.get('content') or _default_recipe
        path.write(yaml.dump(content))

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
    (
        [
            {
                'project': 'mock',
                'arguments': {'mock_argument': 'mock'}
            },
            {
                'action': 'mock_action',
                'arguments': {'mock_argument': 'mock_action_argument'}
            }
        ],
        None.__class__
    ),
])
def test_validate_recipe(tmpdir, mock_recipe, kwargs, expected):
    if issubclass(expected, Exception):
        with pytest.raises(expected):
            mock_recipe.validate_recipe(kwargs)
    else:
        mock_recipe.validate_recipe(kwargs)
        assert mock_recipe.project_arguments is not None


@pytest.mark.parametrize('kwargs,expected', [
    (
        {
            'file_name': 'mock_file.mock'
        },
        MozbitbarRecipeException
    ),
    (
        {
            'content': '````invalid_yaml````',
            'file_name': 'invalid_yaml.file'
        },
        MozbitbarRecipeException
    ),
    (
        {
            'content': """{'project': 'existing'}""",
            'file_name': 'valid.yaml'
        },
        None.__class__
    )
])
def test_load_recipe_from_yaml(tmpdir, mock_recipe, kwargs, expected):
    with mock.patch.object(Recipe, 'validate_recipe', return_value=None):
        mock_file_name = kwargs.get('file_name') or 'mock_recipe.yaml'
        path = tmpdir.mkdir('mock').join(mock_file_name)

        content = kwargs.get('content') or '`invalid_yaml_text'
        path.write(content)
        mock_recipe.recipe_path = path.strpath

        if issubclass(expected, Exception):
            with pytest.raises(expected) as exc:
                mock_recipe.load_recipe_from_yaml()
            assert 'Invalid YAML file' in exc.value.message
        else:
            mock_recipe.load_recipe_from_yaml()


@pytest.mark.parametrize('kwargs,expected', [
    (
        {},
        (
            TypeError,
            'Recipe task list must be of type list.'
        )
    ),
    (
        ['action', 'mock'],
        (
            TypeError,
            'Recipe action must be of type dict.'
        )
    ),
    (
        [
            {
                'argument': 'mock_argument'
            }
        ],
        (
            MozbitbarRecipeException,
            'Recipe action must contain key value: action.'
        )
    )
])
def test_property_task_list(mock_recipe, kwargs, expected):
    with pytest.raises(expected[0]) as exc:
        mock_recipe.task_list = kwargs
    assert expected[1] in (exc.value.args or exc.value.message)


@pytest.mark.parametrize('kwargs,expected', [
    (
        [{
            'project': 'mock',
            'arguments': {'mock_argument': 'mock'}
        },
            {
            'action': 'mock_action',
            'arguments': {'mock_argument': 'mock_action_argument'}
        }],
        None.__class__
    ),
    (
        [{
            'action': 'mock_action',
            'arguments': {'mock_argument': 'mock_action_argument'}
        }],
        MozbitbarRecipeException
    )
])
def test_init(tmpdir, kwargs, expected):
    path = tmpdir.mkdir('mock').join('mock_recipe.yaml')
    content = kwargs or _default_recipe
    path.write(yaml.dump(content))

    if issubclass(expected, Exception):
        with pytest.raises(expected):
            recipe_object = Recipe(path.strpath)
    else:
        recipe_object = Recipe(path.strpath)
        assert recipe_object.project
        assert recipe_object.project_arguments
        assert recipe_object.task_list
