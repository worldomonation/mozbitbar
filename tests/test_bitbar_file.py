# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import random
import string

import mock
import pytest

from mozbitbar import MozbitbarFileException
from mozbitbar.bitbar_project import BitbarProject
from testdroid import Testdroid as Bitbar
from testdroid import RequestResponseError


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
    ('mock_file.zip', False)
])
def test_bb_file_on_local_disk(file_name, expected, initialize_project):
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


@pytest.mark.parametrize('path,expected', [
    (
        '/mock_path/',
        MozbitbarFileException
    ),
    (
        'mock_file',
        ''.join([random.choice(string.lowercase) for _ in range(10)])
    )
])
def test_bb_file_open_file(tmpdir, initialize_project, path, expected):
    if expected == MozbitbarFileException:
        with pytest.raises(expected) as exc:
            initialize_project._open_file(path)
        assert 'could not be located' in exc.value.message
    else:
        path = tmpdir.mkdir('mock').join(path)
        path.write(expected)

        output = initialize_project._open_file(path.strpath)
        assert output
        assert output == expected


@pytest.mark.parametrize('kwargs,expected', [
    (
        {'mock_filename': 'mock_test'},
        MozbitbarFileException
    ),
    (
        {'application_filename': 'mock_path'},
        MozbitbarFileException
    ),
    (
        {'application_filename': 'mock_file'},
        None
    ),
    (
        {'application_filename': 'mocked_application_file.apk'},
        None
    ),
    (
        {'application_filename': 'fail_upload.zip'},
        MozbitbarFileException
    )
])
def test_bb_file_upload_file(tmpdir, initialize_project, kwargs, expected):
    if expected == MozbitbarFileException:
        with pytest.raises(expected):
            if 'fail_upload.zip' in kwargs.values():
                with mock.patch.object(Bitbar,
                                       'upload',
                                       side_effect=RequestResponseError(
                                           'error uploading',
                                           404)):
                    path = tmpdir.mkdir('mock').join(kwargs.values()[0])
                    path.write(' ')

                    initialize_project.upload_file(
                        **{kwargs.keys()[0]: path.strpath})
            else:
                initialize_project.upload_file(**kwargs)
    else:
        path = tmpdir.mkdir('mock').join(kwargs.values()[0])
        path.write(' ')

        initialize_project.upload_file(**{kwargs.keys()[0]: path.strpath})
