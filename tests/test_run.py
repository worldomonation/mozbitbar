# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import pytest
import yaml

from mozbitbar.recipe import Recipe
from mozbitbar.run import initialize_bitbar


_default_recipe = [{
    'project': 'existing',
    'arguments': {
        'project_id': 11,
        'project_name': 'mock_project'
    }
}]


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
