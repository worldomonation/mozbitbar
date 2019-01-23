# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import pytest
import yaml

from mozbitbar import cli
from mozbitbar.run import run_recipe


@pytest.mark.parametrize('credentials', [
    (
        {
            'TESTDROID_URL': 'https://mock.com',
            'TESTDROID_APIKEY': 'mock_api_key'
        },
    )
])
def test_bitbar_init_with_credentials(tmpdir, base_recipe, write_tmp_file,
                                      credentials):
    cli_argument = []

    # set up test credential file
    credentials_path = tmpdir.mkdir('int_test').join('test_credentials.yaml')
    credentials_path.write(yaml.dump(credentials))

    # write a default recipe
    recipe_path = write_tmp_file(base_recipe)

    # formulate the simulated cli commands
    cli_argument.extend(['-c', credentials_path.strpath])
    cli_argument.extend(['-r', recipe_path.strpath])

    # kick off integration test, assertions are built in to the code
    args = cli.cli(cli_argument)
    run_recipe(recipe_path.strpath, args)
