from __future__ import print_function, absolute_import

import string

import pytest

from mozbitbar.bitbar_project import BitbarProject
from mozbitbar import FileException


@pytest.fixture()
def initialize_project():
    return BitbarProject('existing', **{'name': 'mock_project'})


@pytest.mark.parametrize('file_name,expected', [
    ('mock_file.zip', True),
    ('mocked_application_file.apk', True),
    (string.lowercase, False),
    ('1', False)
])
def test_bb_file_on_bitbar(file_name, expected, initialize_project):
    assert initialize_project._file_on_bitbar(file_name) == expected


@pytest.mark.parametrize('file_name,expected', [
    ('mock_file_name', False),
    (None, AssertionError),
    (-1, AssertionError)
])
def test_bb_file_on_bitbar_parameter_is_string(file_name, expected, initialize_project):
    if type(file_name) is not str:
        with pytest.raises(expected):
            initialize_project._file_on_bitbar(file_name)
    else:
        assert initialize_project._file_on_bitbar(file_name) == expected