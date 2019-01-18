# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import pytest
import yaml

from mozbitbar.recipe import Recipe
from mozbitbar.run import run_recipe
from tests.test_run import _default_recipe

# Integration test - tests the entire workflow after CLI parsing #


@pytest.mark.parametrize('test_recipe', [
    [
        {
            'action': 'set_device',
            'arguments': {
                'device': 'mock_device_3'
            }
        },
        {
            'action': 'set_project_framework',
            'arguments': {
                'framework': 2
            }
        },
        {
            'action': 'start_test_run',
            'arguments': {
                'name': 'should_successfully_run_test'
            }
        }
    ],
    [
        {
            'action': 'set_device_group',
            'arguments': {
                'group': 'second_mock_group'
            }
        },
        {
            'action': 'set_project_framework',
            'arguments': {
                'framework': 'mock_framework'
            }
        },
        {
            'action': 'start_test_run',
            'arguments': {
                'name': 'should_successfully_run_test'
            }
        }
    ],
])
def test_run_recipe(tmpdir, test_recipe):
    _integration_test_recipe = _default_recipe[:]
    _integration_test_recipe.extend(test_recipe)

    recipe_name = 'mock_recipe.yaml'
    path = tmpdir.mkdir('mock').join(recipe_name)
    path.write(yaml.dump(_integration_test_recipe))

    run_recipe(path.strpath)
