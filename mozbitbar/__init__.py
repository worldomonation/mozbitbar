# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import


class ProjectException(Exception):
    def __init__(self, message):
        """ProjectException will be raised if any exceptions occur
        relating to project attributes.
        """
        pass


class DeviceException(Exception):
    def __init__(self, message):
        """DeviceException will be raised if any exceptions occur relating to
        device operations.
        """
        pass


class InvalidRecipeException(Exception):
    def __init__(self, message):
        """InvalidRecipeException will be raised upon YAML recipe having
        any errors.
        """
        pass


class FrameworkException(Exception):
    def __init__(self, message):
        pass


class FileException(Exception):
    def __init__(self, message):
        """FileException will be raised if errors relating to file
        transactions occur.
        """
        pass


class CredentialException(Exception):
    def __init__(self, message):
        """CredentialException will be raised if credentials supplied to
        BitbarProject has issues.
        """
        pass


class OperationNotImplementedException(Exception):
    def __init__(self, message):
        """OperationNotImplementedException will be raised if a recipe action
        does not correspond to an implemented method in the BitbarProject
        object.
        """
        pass


class TestException(Exception):
    def __init__(self, message):
        """TestException will be raised if test runs experience any sort of
        errors.
        """
        pass
