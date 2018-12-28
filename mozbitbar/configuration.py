# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import os
import sys

from mozbitbar import MozbitbarCredentialException
from testdroid import Testdroid, RequestResponseError


class Configuration(object):
    def __init__(self, **kwargs):
        """Initializes the Configuration class, in one of two ways:
            - using kwargs: user-provided dictionary of required parameters.
            - using envvar: parses the environment variables set on
            host machine.

        Either methods are supported. By default, the environment variable
        approach is preferred.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Raises:
            MozbitbarCredentialException: If minimum required credentials
                were not set, or supplied credentials were invalid.
        """
        if kwargs and any(['TESTDROID' in key for key in kwargs.keys()]):
            self.user_name = kwargs.get('TESTDROID_USERNAME')
            self.user_password = kwargs.get('TESTDROID_PASSWORD')
            self.api_key = kwargs.get('TESTDROID_APIKEY')
            self.url = kwargs.get('TESTDROID_URL')
        else:
            self.user_name = os.getenv('TESTDROID_USERNAME')
            self.user_password = os.getenv('TESTDROID_PASSWORD')
            self.api_key = os.getenv('TESTDROID_APIKEY')
            self.url = os.getenv('TESTDROID_URL')

        # ensure minimal viable set of parameters are set.
        try:
            assert (self.user_name and self.user_password) or self.api_key
            assert self.url
        except AssertionError:
            msg = '{}: failed assertion of Bitbar configuration values'
            raise MozbitbarCredentialException(msg)
        except AttributeError as ae:
            raise MozbitbarCredentialException(ae.message)

        # instantiate client.
        self.client = Testdroid(username=self.user_name or None,
                                password=self.user_password or None,
                                apikey=self.api_key or None,
                                url=self.url)

        # make a simple call to verify parameters are valid.
        try:
            self.client.get_me()
        except RequestResponseError as rre:
            msg = '''Bitbar rejected supplied credentials.
                     Check the supplied **kwargs or environment variables.'''
            raise MozbitbarCredentialException(msg, rre.status_code)
