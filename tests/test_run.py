# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import pytest
import yaml

from mozbitbar.recipe import Recipe
from mozbitbar.run import initialize_bitbar, initialize_recipe

# TODO: This is messy. Either throw it into conftest and make it available
# everywhere, or imitate test_run_integration.py for it.
_default_recipe = [{
    'project': 'existing',
    'arguments': {
        'project_id': 11,
        'project_name': 'mock_project'
    }
}]

_recipe_with_action = _default_recipe[:]
mock_action = {
    'action': 'mock_action',
    'arguments': {
        'mock_argument': 'mock_value'
    }
}
_recipe_with_action.append(mock_action)


def write_tmp_recipe(tmpdir, recipe):
    recipe_name = 'mock_recipe.yaml'
    path = tmpdir.mkdir('mock').join(recipe_name)
    path.write(yaml.dump(recipe))
    return path


@pytest.mark.parametrize('recipe,expected', [
    (
        _default_recipe,
        {
            'task_list': [],
            'project': 'existing',
            'project_arguments': {
                'project_id': 11,
                'project_name': 'mock_project'
            }
        }
    ),
    (
        _recipe_with_action,
        {
            'task_list': [
                {
                    'action': 'mock_action',
                    'arguments': {
                        'mock_argument': 'mock_value'
                    }
                }
            ]
        }
    ),
])
def test_initialize_recipe(tmpdir, recipe, expected):
    path = write_tmp_recipe(tmpdir, recipe)
    obj = initialize_recipe(path.strpath)
    for key, value in expected.iteritems():
        assert getattr(obj, key) == value


@pytest.mark.parametrize('recipe,expected', [
    (
        _default_recipe,
        {
            'project_name': 'mock_project',
            'project_id': 11,
        }
    ),
    (
        [{
            'project': 'existing',
            'arguments': {
                'project_id': 10000
            }
        }],
        {
            'project_name': 'yet_another_mock_project',
            'project_id': 10000
        }
    )
])
def test_initialize_bitbar(tmpdir, recipe, expected):
    recipe_name = 'mock_recipe.yaml'
    path = tmpdir.mkdir('mock').join(recipe_name)
    path.write(yaml.dump(recipe))

    obj = initialize_bitbar(Recipe(path.strpath))
    for key, value in expected.iteritems():
        assert getattr(obj, key) == value
