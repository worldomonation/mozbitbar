# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

class ProjectException(Exception):
    def __init__(self, message):
        super(ProjectException, self).__init__(message)

class InvalidRecipeException(Exception):
    def __init__(self, message):
        super(InvalidRecipeException, self).__init__(message)

class FrameworkException(Exception):
    def __init__(self, message):
        super(FrameworkException, self).__init__(message)

class FileException(Exception):
    def __init__(self, message):
        super(FileException, self).__init__(message)
