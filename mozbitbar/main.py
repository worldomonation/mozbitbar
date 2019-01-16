# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import os
import sys

try:
    from mozbitbar.recipe_handler import run_recipe
    from mozbitbar.log import setup_logger
    from mozbitbar.cli import cli
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    from recipe_handler import run_recipe
    from log import setup_logger
    from cli import cli


def main():
    # example of how to call and use Bitbar with this harness.
    # in a taskcluster/treeherder environment, the script will
    # call these methods instead of instead of main().
    args = cli()
    setup_logger(**vars(args))
    run_recipe(args.recipe)


if __name__ == '__main__':
    main()
