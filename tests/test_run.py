# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import pytest
import yaml

from mozbitbar.recipe import Recipe
from mozbitbar.run import initialize_bitbar, initialize_recipe


# def write_tmp_recipe(tmpdir, recipe):
#     recipe_name = 'mock_recipe.yaml'
#     path = tmpdir.mkdir('mock').join(recipe_name)
#     path.write(yaml.dump(recipe))
#     return path


@pytest.mark.parametrize('additional_actions,expected', [
    (
        None,
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
        {
            'action': 'mock_action',
            'arguments': {
                'mock_argument': 'mock_value'
            }
        },
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
def test_initialize_recipe(write_tmp_recipe, base_recipe, additional_actions, expected):
    if additional_actions:
        base_recipe.append(additional_actions)

    path = write_tmp_recipe(base_recipe)
    obj = initialize_recipe(path.strpath)
    for key, value in expected.iteritems():
        assert getattr(obj, key) == value


@pytest.mark.parametrize('recipe_under_test,expected', [
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
def test_initialize_bitbar(write_tmp_recipe, recipe_under_test, expected):
    path = write_tmp_recipe(recipe_under_test)

    obj = initialize_bitbar(Recipe(path.strpath))
    for key, value in expected.iteritems():
        assert getattr(obj, key) == value
