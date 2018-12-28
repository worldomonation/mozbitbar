# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import sys

from mozbitbar import recipe_handler
from mozbitbar.cli import cli

from mozbitbar import log
logger = log.setup_logger()


def main():
    # example of how to call and use Bitbar with this harness.
    # in a taskcluster/treeherder environment, the script will
    # call these methods instead of instead of main().
    recipe_name = cli(sys.argv[1:])
    recipe_handler.run_recipe(recipe_name)


if __name__ == '__main__':
    main()
