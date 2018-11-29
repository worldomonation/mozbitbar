# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import


class ProjectException(Exception):
    def __init__(self, message):
        """ProjectException will be raised if any exceptions occur
        relating to project attributes.
        """
        super(ProjectException, self).__init__(message)


class InvalidRecipeException(Exception):
    def __init__(self, message):
        """InvalidRecipeException will be raised upon YAML recipe having
        any errors.
        """
        super(InvalidRecipeException, self).__init__(message)


class FrameworkException(Exception):
    def __init__(self, message):
        super(FrameworkException, self).__init__(message)


class FileException(Exception):
    def __init__(self, message):
        """FileException will be raised if errors relating to file
        transactions occur.
        """
        super(FileException, self).__init__(message)


class CredentialException(Exception):
    def __init__(self, message):
        """CredentialException will be raised if credentials supplied to
        BitbarProject has issues.
        """
        super(CredentialException, self).__init__(message)


class OperationNotImplementedException(Exception):
    def __init__(self, message):
        """OperationNotImplementedException will be raised if a recipe action
        does not correspond to an implemented method in the BitbarProject
        object.
        """
        super(OperationNotImplementedException, self).__init__(message)
