# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

class NotInitializedException(Exception):
      def __init__(self, message):
          super(NotInitializedException, self).__init__(message)

class InvalidRecipeException(Exception):
    def __init__(self, message):
            super(NotInitializedException, self).__init__(message)
