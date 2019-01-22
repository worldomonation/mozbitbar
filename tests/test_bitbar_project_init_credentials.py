# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import pytest
import yaml

from mozbitbar import cli
from mozbitbar.run import run_recipe

_default_recipe = [{
    'project': 'existing',
    'arguments': {
        'project_id': 10101010,
        'project_name': 'mock_project'
    }
}]

_test_credential_file = 'test_credential_file.yaml'


@pytest.fixture
def default_recipe_path(tmpdir):
    path = tmpdir.mkdir('default_recipe').join('default_recipe.yaml')
    path.write(yaml.dump(_default_recipe))

    return path.strpath


@pytest.mark.parametrize('credentials', [
    (
        {
            'TESTDROID_URL': 'https://mock.com',
            'TESTDROID_APIKEY': 'mock_api_key'
        },
    )
])
def test_bitbar_init_with_credentials(tmpdir, default_recipe_path,
                                      credentials):
    cli_argument = []

    # set up recipe first using the fixture
    cli_argument.extend(['-r', default_recipe_path])

    # set up test credential file
    path = tmpdir.mkdir('mock').join(_test_credential_file)
    path.write(yaml.dump(credentials))
    cli_argument.extend(['-c', path.strpath])

    # kick off integration test, assertions are built in to the code
    args = cli.cli(cli_argument)
    run_recipe(default_recipe_path, args)
