# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import


class MozbitbarBaseException(Exception):
    def __init__(self, **kwargs):
        """MozbitbarBaseException is the base class from which all custom
        Mozbitbar exceptions inherit from. It in turn inherits from the base
        Exception class in Python.

        Args:
            **kwargs: Arbitrary keyword arguments.
        """
        self.message = kwargs.pop('message', None)
        self.status_code = kwargs.pop('status_code', None)


class MozbitbarProjectException(MozbitbarBaseException):
    def __init__(self, **kwargs):
        """MozbitbarProjectException will be raised if any exceptions occur
        relating to project attributes.
        """
        super(MozbitbarProjectException, self).__init__(**kwargs)


class MozbitbarDeviceException(MozbitbarBaseException):
    def __init__(self, **kwargs):
        """MozbitbarDeviceException will be raised for any exceptions relating
        to device, device groups or device operations.
        """
        super(MozbitbarDeviceException, self).__init__(**kwargs)


class MozbitbarRecipeException(MozbitbarBaseException):
    def __init__(self, **kwargs):
        """MozbitbarRecipeException will be raised upon the recipe having any
        sort of errors.
        """
        super(MozbitbarRecipeException, self).__init__(**kwargs)


class MozbitbarFrameworkException(MozbitbarBaseException):
    def __init__(self, **kwargs):
        """FrameworkException is raised when Bitbar project framework
        encounters an issue.
        """
        super(MozbitbarFrameworkException, self).__init__(**kwargs)


class MozbitbarFileException(MozbitbarBaseException):
    def __init__(self, path, **kwargs):
        """MozbitbarFileException will be raised if errors relating to file
        transactions occur.
        """
        super(MozbitbarFileException, self).__init__(**kwargs)
        self.path = path


class MozbitbarCredentialException(MozbitbarBaseException):
    def __init__(self, **kwargs):
        """MozbitbarCredentialException will be raised if credentials
        supplied to BitbarProject has issues.

        Args:
            message (str): Exception message.
            status_code (int, optional): HTTP status code from Testdroid.
        """
        super(MozbitbarCredentialException, self).__init__(**kwargs)


class MozbitbarTestRunException(MozbitbarBaseException):
    def __init__(self, **kwargs):
        """MozbitbarTestRunException will be raised if Bitbar test runs experience
        any sort of issues.
        """
        super(MozbitbarTestRunException, self).__init__(**kwargs)
        self.test_run_id = kwargs.pop('test_run_id', None)
        self.test_run_name = kwargs.pop('test_run_name', None)


class MozbitbarOperationNotImplementedException(MozbitbarBaseException):
    def __init__(self, **kwargs):
        """MozbitbarOperationNotImplementedException will be raised if a
        recipe action does not correspond to an implemented method in the
        BitbarProject object.
        """
        super(MozbitbarOperationNotImplementedException, self).__init__(
            **kwargs)
