from __future__ import print_function, absolute_import

import sys

from argparse import ArgumentParser

import testdroid


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
