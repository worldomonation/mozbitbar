from __future__ import print_function, absolute_import

import os
import requests

from time import time

from testdroid import Testdroid, RequestResponseError

class Configuration(object):
    def __init__(self, **kwargs):
        """Initializes the Configuration class, in one of two ways:
            - via kwargs: user-provided dictionary of required parameters.
            - via envvar: parses the environment variables set on host machine.
        """
        if kwargs:
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
            raise EnvironmentError()

        # instantiate client.
        self.client = Testdroid(username=self.user_name,
                                password=self.user_password,
                                apikey=self.api_key,
                                url=self.url)

        # make a simple call to verify parameters are valid.
        try:
            self.client.get_token()
        except RequestResponseError:
            print('Incorrect values provided to Testdroid.\nPlease ensure' +
                  'username, password and/or API key as well as Bitbar URL is set.')
            raise EnvironmentError()
