from __future__ import absolute_import

import os
import requests

from time import time


class Configuration(object):
    def __init__(self, **kwargs):
        if kwargs:
            self.user_name = kwargs.get('TESTDROID_USERNAME')
            self.user_password = kwargs.get('TESTDROID_PASSWORD')
            self.url = kwargs.get('TESTDROID_URL')
        else:
            self.user_name = os.getenv('TESTDROID_USERNAME')
            self.user_password = os.getenv('TESTDROID_PASSWORD')
            self.url = os.getenv('TESTDROID_URL', '')

        if None in (self.user_name, self.user_password):
            raise EnvironmentError()


class Auth(Configuration):
    def __init__(self, config):
        self.access_token = ''
        self.refresh_token = ''
        self.access_token_expire_ts = 0
        self.auth_url = '{}/oauth/token'.format(config.url)

        self.authenticate(config)

    def decode_response(self, response):
        assert response.status_code in list(range(200, 300))

        self.access_token = response.json()['access_token']
        self.refresh_token = response.json()['refresh_token']
        self.access_token_expire_ts = time() + response.json()['expires_in']

    def token_expired(self):
        return time() > self.access_token_expire_ts

    def authenticate(self, config):
        if not self.access_token:
            payload = {
                "client_id": "testdroid-cloud-api",
                "grant_type": "password",
                "username": config.user_name,
                "password": config.user_password,
            }
        elif self.access_token and self.token_expired():
            payload = {
                "client_id": "testdroid-cloud-api",
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            }
        response = requests.post(
            url=self.auth_url,
            data=payload,
            headers={"Accept": "application/json"}
        )
        self.decode_response(response)
