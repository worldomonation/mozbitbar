# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import random
import string

import pytest

from mozbitbar import MozbitbarFileException
from mozbitbar.bitbar_project import BitbarProject


@pytest.fixture()
def initialize_project():
    # initialize a dummy project for when the __init__ method is not
    # under test.
    kwargs = {
        'project_name': 'mock_project',
        'TESTDROID_USERNAME': 'MOCK_ENVIRONMENT_VALUE_TEST',
        'TESTDROID_PASSWORD': 'MOCK_ENVIRONMENT_VALUE_TEST',
        'TESTDROID_APIKEY': 'MOCK_ENVIRONMENT_VALUE_TEST',
        'TESTDROID_URL': 'https://www.mock_test_env_var.com',
    }
    return BitbarProject('existing', **kwargs)


@pytest.mark.parametrize('file_name,expected', [
    ('mock_file.zip', False),
    ('mock_file.apk', True)
])
def test_bb_file_on_local_disk(write_tmp_file, file_name, expected,
                               initialize_project):
    if expected:
        path = write_tmp_file(' ')
        file_name = path.strpath

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
    (
        '/mock_path/',
        MozbitbarFileException
    ),
    (
        'mock_file',
        ''.join([random.choice(string.lowercase) for _ in range(10)])
    )
])
def test_bb_file_open_file(tmpdir, initialize_project, file_name, expected):
    if expected == MozbitbarFileException:
        with pytest.raises(expected) as exc:
            initialize_project._open_file(file_name)
        assert 'could not be located' in exc.value.message
    else:
        path = tmpdir.mkdir('mock').join(file_name)
        path.write(expected)

        output = initialize_project._open_file(path.strpath)
        assert output
        assert output == expected


@pytest.mark.parametrize('kwargs,expected', [
    (
        {'mock_filename': 'invalid_file_type'},
        MozbitbarFileException
    ),
    (
        {'application_filename': 'invalid_path'},
        MozbitbarFileException
    ),
    (
        {'application_filename': 'mock_application_file.apk'},
        None
    ),
    (
        {'test_filename': 'mock_test_file.rar'},
        None
    ),
    (
        {'data_filename': 'mock_data_file.tar.gz'},
        None
    ),
    (
        # intentional failure - implemented in conftest
        {'application_filename': 'fail_upload.zip'},
        MozbitbarFileException
    )
])
def test_bb_file_upload_file(write_tmp_file, initialize_project,
                             kwargs, expected):
    if type(expected) == type:
        with pytest.raises(expected):
            initialize_project.upload_file(**kwargs)
    else:
        file_type, file_name = kwargs.popitem()
        path = write_tmp_file(' ', file_path=file_name)

        initialize_project.upload_file(**{file_type: path.strpath})
