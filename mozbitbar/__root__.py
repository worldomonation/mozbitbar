from __future__ import print_function, absolute_import

import os


def path():
    """Returns the absolute path to the root of mozbitbar source code
    directory.

    Returns:
        str: Absolute path to the mozbitbar source code directory.
    """
    return os.path.join(os.path.dirname(__file__), '')
