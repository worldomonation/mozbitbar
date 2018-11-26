from __future__ import print_function, absolute_import

import pytest

from mozbitbar.configuration import Configuration


def test_this(mock_testdroid_client):
    print(mock_testdroid_client.username)
    assert False

