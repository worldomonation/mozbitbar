# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

from mozbitbar.configuration import Configuration


class Bitbar(Configuration):
    """Bitbar is a class which represents an instance of Bitbar.

    In a distinction from BitbarProject, methods implemented in
    Bitbar can be called without requiring a project id.
    """
    def __init__(self):
        """Initializes the Bitbar class.
        """
        super(Bitbar, self).__init__()
