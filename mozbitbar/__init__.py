# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import


class MozbitbarProjectException(Exception):
    def __init__(self, message):
        """MozbitbarProjectException will be raised if any exceptions occur
        relating to project attributes.
        """
        pass


class MozbitbarDeviceException(Exception):
    def __init__(self, message):
        """MozbitbarDeviceException will be raised if any exceptions occur relating to
        device operations.
        """
        pass


class MozbitbarInvalidRecipeException(Exception):
    def __init__(self, message):
        """MozbitbarInvalidRecipeException will be raised upon YAML recipe having
        any errors.
        """
        pass


class MozbitbarFrameworkException(Exception):
    def __init__(self, message):
        pass


class MozbitbarFileException(Exception):
    def __init__(self, message):
        """MozbitbarFileException will be raised if errors relating to file
        transactions occur.
        """
        pass


class MozbitbarCredentialException(Exception):
    def __init__(self, message):
        """MozbitbarCredentialException will be raised if credentials supplied to
        BitbarProject has issues.
        """
        pass


class MozbitbarTestException(Exception):
    def __init__(self, message):
        """MozbitbarTestException will be raised if Bitbar test runs experience
        any sort of issues.
        """
    pass


class OperationNotImplementedException(Exception):
    def __init__(self, message):
        """OperationNotImplementedException will be raised if a recipe action
        does not correspond to an implemented method in the BitbarProject
        object.
        """
        pass
