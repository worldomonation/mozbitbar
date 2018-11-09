from __future__ import print_function, absolute_import

import sys

from mozbitbar.cli import cli
from mozbitbar.recipe_handler import run_recipes


def main():
    recipe_name = cli(sys.argv[1:])

    if recipe_name:
        run_recipes(recipe_name)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
