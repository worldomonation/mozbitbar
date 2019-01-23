# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import pytest
import yaml

from mozbitbar.run import run_recipe
from argparse import Namespace

# Integration test - tests the entire workflow after CLI parsing #


@pytest.mark.parametrize('test_recipe,expected', [
    (
        # set device and framework by id
        [
            {
                'action': 'set_device',
                'arguments': {
                    'device': 717
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
        None
    ),
    (
        # set device group and framework by name
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
        None
    ),
    (
        # action that does not exist - resulting in SystemExit
        [
            {
                'action': 'nonexistent_action',
                'arguments': {
                    'invalid_argument': 'invalid_argument_value'
                }
            }
        ],
        SystemExit
    ),
    (
        # no action list - will not run anything
        [],
        None
    ),
    (
        # set_device action raises an exception resulting in SystemExit
        [
            {
                'action': 'set_device',
                'arguments': {
                    'device': 'non_existent_device'
                }
            }
        ],
        SystemExit
    ),
    (
        # set_project_parameters returns RequestResponseError re-raised as
        # MozbitbarProjectException resulting in SystemExit
        [
            {
                'action': 'set_project_parameters',
                'arguments': {
                    'parameters': [
                        {
                            'key': 'unacceptable_key',
                            'value': 'unacceptable_value'
                        }
                    ]
                }
            }
        ],
        SystemExit
    )
])
def test_integration_recipe(tmpdir, base_recipe, test_recipe, expected):
    base_recipe.extend(test_recipe)

    recipe_name = 'mock_recipe.yaml'
    path = tmpdir.mkdir('mock').join(recipe_name)
    path.write(yaml.dump(base_recipe))

    if type(expected) == type:
        # exceptions evaluate to `type`
        with pytest.raises(expected) as ex:
            run_recipe(path.strpath, Namespace(credentials=None))
        assert expected == ex.type
        assert ex.tb is not None
    else:
        run_recipe(path.strpath, Namespace(credentials=None))
