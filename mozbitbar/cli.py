# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

from argparse import ArgumentParser


def parser_arguments(args):
    parser = ArgumentParser('Runs Testdroid tasks.')
    parser.add_argument('-r', '--recipe')

    args, remainder = parser.parse_known_args()

    return args, remainder


def cli(args):
    args, remainder = parser_arguments(args)

    if args.recipe:
        return args.recipe

    return None
