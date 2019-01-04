# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import string

import pytest

from mozbitbar.bitbar_project import BitbarProject


@pytest.fixture()
def initialize_project():
    return BitbarProject('existing', **{'project_name': 'mock_project'})


@pytest.mark.parametrize('file_name,expected', [
    ('mock_file.zip', False),
    pytest.param('test_bitbar_file.py', True, marks=pytest.mark.xfail)
])
def test_bb_file_on_local_disk(file_name, expected, initialize_project):
    # TODO: stub test
    assert initialize_project._file_on_local_disk(file_name) == expected


@pytest.mark.parametrize('file_name,expected', [
    ('mock_file.zip', True),
    ('mocked_application_file.apk', True),
    (string.lowercase, False),
    ('1', False),
    (None, False),
    (-1, False)
])
def test_bb_file_on_bitbar(file_name, expected, initialize_project):
    assert initialize_project._file_on_bitbar(file_name) == expected


@pytest.mark.parametrize('file_name,expected', [
    ('mock_file.zip', False),
])
def test_bb_file_upload(file_name, expected, initialize_project):
    # TODO: stub test
    assert file_name
