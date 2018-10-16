from __future__ import absolute_import

from time import time

import pytest

from mozbitbar.configuration import Configuration, Auth

def test_configuration_initialize():
    config = Configuration()

    assert config.user_name is not None
    assert config.user_password is not None


def test_auth_initialize():
    config = Configuration()

    auth_obj = Auth(config)

    assert auth_obj.access_token != None
    assert auth_obj.refresh_token != None
    assert auth_obj.access_token_expire_ts >= time()

def test_auth_refresh_token():
    config = Configuration()

    auth_obj = Auth(config)
    auth_obj.access_token_expire_ts = time() - 200000

    assert auth_obj.access_token_expire_ts < time()
    assert auth_obj.token_expired()
    old_access_token = auth_obj.access_token

    auth_obj.authenticate(config)

    assert auth_obj.access_token_expire_ts >= time()
    assert auth_obj.access_token != old_access_token
