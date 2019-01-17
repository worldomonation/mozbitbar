# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import sys
from argparse import ArgumentParser

_parser = None


def get_parser():
    global _parser

    if _parser is None:
        _parser = ArgumentParser(description='Runs Testdroid tasks.')
        _parser.add_argument('-r', '--recipe',
                             help='Specifies a recipe to load from disk.')
        _parser.add_argument('-v', '--verbose', action='store_true',
                             help='Enables debugging output.')
        _parser.add_argument('-q', '--quiet', action='store_true',
                             help='Disables all output except warning and \
                             higher.')
    return _parser


def parse_arguments(args):
    parser = get_parser()
    args, remainder = parser.parse_known_args(args)

    return args, remainder


def cli(cli_args=sys.argv[1:]):
    args, _ = parse_arguments(cli_args)
    return args
