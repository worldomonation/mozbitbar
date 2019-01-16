# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import logging
import os

from testdroid import RequestResponseError, Testdroid

try:
    from mozbitbar import MozbitbarCredentialException
except ImportError:
    from __init__ import MozbitbarCredentialException


logger = logging.getLogger('mozbitbar')


class Configuration(object):
    def __init__(self, **kwargs):
        """Initializes the Configuration class, in one of two ways:
            - using kwargs: user-provided dictionary containing key/value
                pairs. Keys are expected to be named in same manner as
                using environment variables.
            - using envvar: parses the environment variables set on
            host machine.

        Either methods are supported. By default, the environment variable
        approach is prioritized.

        For reference on how to name the environment variables, please refer
        to Testdroid documentation at
        https://github.com/bitbar/testdroid-api-client-python#usage

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

        if not ((self.user_name and self.user_password) or self.api_key):
            msg = 'Missing Testdroid credentials. \
                   Check username/password or apikey value.'
            raise MozbitbarCredentialException(message=msg)

        if not self.url:
            msg = 'Missing Testdroid cloud URL. Check url value.'
            raise MozbitbarCredentialException(message=msg)

        # instantiate client.
        self.client = Testdroid(username=self.user_name or None,
                                password=self.user_password or None,
                                apikey=self.api_key or None,
                                url=self.url)

        # make a simple call to verify parameters are valid.
        try:
            self.client.get_me()
        except RequestResponseError as rre:
            raise MozbitbarCredentialException(message=rre.message,
                                               status_code=rre.status_code)
