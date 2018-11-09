from __future__ import print_function, absolute_import

import os
import sys

import yaml

from testdroid import Testdroid

from mozbitbar.cli import cli
from mozbitbar.recipe_handler import run_recipes


def main():
    cli_argument = cli(sys.argv[1:])
    run_recipes(cli_argument)


if __name__ == '__main__':
    main()
