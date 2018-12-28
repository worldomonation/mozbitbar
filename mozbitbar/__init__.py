# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

from mozbitbar import log
logger = log.setup_logger()


class MozbitbarProjectException(Exception):
    def __init__(self, message):
        """MozbitbarProjectException will be raised if any exceptions occur
        relating to project attributes.
        """
        self.message = message


class MozbitbarDeviceException(Exception):
    def __init__(self, message):
        """MozbitbarDeviceException will be raised if any exceptions occur
        relating to device operations.
        """
        self.message = message


class MozbitbarRecipeException(Exception):
    def __init__(self, message):
        """MozbitbarRecipeException will be raised upon YAML recipe
        having any errors.
        """
        self.message = message


class MozbitbarFrameworkException(Exception):
    def __init__(self, message):
        """FrameworkException is raised when project framework encounters
        an issue.
        """
        self.message = message


class MozbitbarFileException(Exception):
    def __init__(self, message, path):
        """MozbitbarFileException will be raised if errors relating to file
        transactions occur.
        """
        self.message = message
        self.path = path


class MozbitbarCredentialException(Exception):
    def __init__(self, message, status_code=None):
        """MozbitbarCredentialException will be raised if credentials
        supplied to BitbarProject has issues.

        Args:
            message (str): Exception message.
            status_code (int, optional): HTTP status code from Testdroid.
        """
        self.message = message
        self.status_code = status_code


class MozbitbarTestRunException(Exception):
    def __init__(self, message, test_run_id):
        """MozbitbarTestRunException will be raised if Bitbar test runs experience
        any sort of issues.
        """
        self.message = message
        self.test_run_id = test_run_id


class MozbitbarOperationNotImplementedException(Exception):
    def __init__(self, message):
        """MozbitbarOperationNotImplementedException will be raised if a
        recipe action does not correspond to an implemented method in the
        BitbarProject object.
        """
        self.message = message
