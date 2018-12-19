# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import os


def path():
    """Returns the absolute path to the root of mozbitbar source code
    directory.

    Returns:
        str: Absolute path to the mozbitbar source code directory.
    """
    return os.path.join(os.path.dirname(__file__), '')
