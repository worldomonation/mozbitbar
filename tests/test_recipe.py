# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import mock

import pytest

from mozbitbar import MozbitbarRecipeException
from mozbitbar.recipe import Recipe


@pytest.fixture(autouse=True)
def mock_recipe_object():
    with mock.patch.object(Recipe, '__init__', return_value=None):
        recipe_obj = Recipe('')
        return recipe_obj


@pytest.mark.parametrize('kwargs,expected', [
    (
        {
            'file_name': 'mock_parametrized_recipe.yaml'
        },
        None
    ),
    (
        {
            'file_name': 'another_mock_file.yaml',
            'content': 'dummy'
        },
        None
    ),
    (
        {
            'file_name': 'mock_recipe_that_does_not_exist.yaml'
        },
        MozbitbarRecipeException
    ),
])
def test_locate_recipe(write_tmp_file, base_recipe, mock_recipe_object, kwargs,
                       expected):
    if type(expected) == type:
        with pytest.raises(expected) as mre:
            mock_recipe_object.locate_recipe(kwargs.get('file_name'))
        assert 'recipe not found' in mre.value.message
    else:
        mock_file_name = kwargs.get('file_name') or 'mock_recipe.yaml'
        path = write_tmp_file(base_recipe, file_path=mock_file_name)

        mock_recipe_object.locate_recipe(path.strpath)

        assert mock_recipe_object.recipe_path == path.strpath
        assert mock_recipe_object.recipe_name == path.basename


@pytest.mark.parametrize('test_recipe,expected', [
    (
        # valid recipe
        [
            {
                'project': 'existing',
                'arguments': {
                    'project_id': 1
                }
            }
        ],
        None
    ),
    (
        # invalid recipe that specifies invalid project
        [
            {
                'project': 'mock',
                'arguments': {}
            }
        ],
        MozbitbarRecipeException
    ),
    (
        # invalid recipe with arguments missing
        [
            {
                'project': 'mock'
            }
        ],
        TypeError
    ),
    (
        # invalid recipe with incorrect data type for arguments
        [
            {
                'project': 'mock',
                'arguments': []
            }
        ],
        TypeError
    ),
    (
        # invalid recipe missing project arguments
        [
            {
                'project': 'mock',
                'arguments': {}
            }
        ],
        MozbitbarRecipeException
    ),
    (
        # invalid recipe missing all required components
        [
            {
                'arguments': {}
            }
        ],
        MozbitbarRecipeException
    ),
    (
        # valid recipe
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
        None
    ),
])
def test_validate_recipe(tmpdir, mock_recipe_object, test_recipe, expected):
    if type(expected) == type:
        with pytest.raises(expected):
            mock_recipe_object.validate_recipe(test_recipe)
    else:
        mock_recipe_object.validate_recipe(test_recipe)
        assert mock_recipe_object.project_arguments is not None


@pytest.mark.parametrize('filename,content,expected', [
    (
        'mock_file.mock',
        '`invalid_yaml_text',
        MozbitbarRecipeException
    ),
    (
        'invalid_yaml.file',
        '````invalid_yaml````',
        MozbitbarRecipeException
    ),
    (
        'valid.yaml',
        """{'project': 'existing'}""",
        None
    )
])
def test_load_recipe_from_yaml(write_tmp_file, mock_recipe_object, filename,
                               content, expected):
    with mock.patch.object(Recipe, 'validate_recipe', return_value=None):
        mock_file_name = filename or 'mock_recipe.yaml'

        # set up mock recipe and set the path of Recipe
        path = write_tmp_file(content, fmt='none', file_path=mock_file_name)
        mock_recipe_object.recipe_path = path.strpath

        if type(expected) == type:
            with pytest.raises(expected) as exc:
                mock_recipe_object.load_recipe_from_yaml()
            assert 'Invalid YAML file' in exc.value.message
        else:
            mock_recipe_object.load_recipe_from_yaml()


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
def test_property_task_list(mock_recipe_object, kwargs, expected):
    with pytest.raises(expected[0]) as exc:
        mock_recipe_object.task_list = kwargs
    assert expected[1] in (exc.value.args or exc.value.message)


@pytest.mark.parametrize('content,expected', [
    (
        [{
            'project': 'mock',
            'arguments': {'mock_argument': 'mock'}
        },
            {
            'action': 'mock_action',
            'arguments': {'mock_argument': 'mock_action_argument'}
        }],
        None
    ),
    (
        [{
            'action': 'mock_action',
            'arguments': {'mock_argument': 'mock_action_argument'}
        }],
        MozbitbarRecipeException
    )
])
def test_init(write_tmp_file, content, expected):
    path = write_tmp_file(content)

    if type(expected) == type:
        with pytest.raises(expected):
            recipe_object = Recipe(path.strpath)
    else:
        recipe_object = Recipe(path.strpath)
        assert recipe_object.project
        assert recipe_object.project_arguments
        assert recipe_object.task_list
