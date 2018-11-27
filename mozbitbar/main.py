from __future__ import print_function, absolute_import

import logging
import sys

from mozbitbar import recipe_handler
from mozbitbar.cli import cli

def main():
    # example of how to call and use Bitbar with this harness.
    # in a taskcluster/treeherder environment, the script will
    # call these methods instead of instead of main().
    recipe_name = cli(sys.argv[1:])
    recipe_handler.run_recipe(recipe_name)


if __name__ == '__main__':
    main()
