# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

from mozbitbar import log
from mozbitbar import recipe_handler
from mozbitbar.cli import cli


def initialize_logging(args=None):
    log.setup_logger(args)


def main():
    # example of how to call and use Bitbar with this harness.
    # in a taskcluster/treeherder environment, the script will
    # call these methods instead of instead of main().
    args = cli()
    initialize_logging(vars(args))
    recipe_handler.run_recipe(args.recipe)


if __name__ == '__main__':
    main()
