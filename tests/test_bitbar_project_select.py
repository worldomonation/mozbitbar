# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import string

import mock
import pytest

from mozbitbar import MozbitbarProjectException
from mozbitbar.bitbar_project import BitbarProject
from testdroid import RequestResponseError
from testdroid import Testdroid as Bitbar


@pytest.fixture
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


# Existing projects #


@pytest.mark.parametrize('kwargs,expected', [
    (
        {
            'project_id': 11
        },
        {
            'id': 11,
            'name': 'mock_project'
        }
    ),
    (
        {
            'project_id': 99
        },
        {
            'id': 99,
            'name': 'another_mock_project'
        }
    ),
    (
        {
            'project_id': 2**32
        },
        MozbitbarProjectException
    ),
    (
        {
            'project_id': -1
        },
        MozbitbarProjectException
    ),
    (
        {
            'project_name': 'mock_project'
        },
        {
            'id': 11,
            'name': 'mock_project'
        }
    ),
    (
        {
            'project_name': 'another_mock_project'
        },
        {
            'name': 'another_mock_project',
            'id': 99
        }
    ),
    (
        {
            'project_name': string.lowercase
        },
        MozbitbarProjectException
    ),
    (
        {
            'project_name': 'None'
        },
        MozbitbarProjectException
    ),
    (
        {
            'project_name': 'mock_project_4'
        },
        {
            'id': 99999,
            'name': 'mock_project_4',
        }
    ),
    (
        {
            'project_id': 11,
            'project_name': 'mock_project'
        },
        {
            'id': 11,
            'name': 'mock_project'
        }
    ),
    (
        {
            'project_id': 11,
            'project_name': 'yet_another_mock_project'
        },
        {
            'id': 10000,
            'name': 'yet_another_mock_project'
        }
    )
])
def test_bb_project_init_existing(kwargs, expected):
    """Ensures BitbarProject is able to retrieve existing project by id
    or name, and process resulting output of the (mocked) call.

    Directly tests methods involved in:
        - initialization of project
        - retrieve and set project parameters by id or name
    """
    if expected is MozbitbarProjectException:
        with pytest.raises(MozbitbarProjectException):
            BitbarProject('existing', **kwargs)

    else:
        project = BitbarProject('existing', **kwargs)
        if expected.get('id'):
            assert project.project_id == expected.get('id')
        if expected.get('project_name'):
            assert project.project_name == expected.get('name')


# Project status #


@pytest.mark.parametrize('project_status,expected', [
    ('present', MozbitbarProjectException),
    ('exist', MozbitbarProjectException),
    ('create', MozbitbarProjectException),
])
def test_bb_project_status(project_status, expected):
    """Ensures BitbarProject raises an exception on invalid project status.
    """
    if expected is MozbitbarProjectException:
        with pytest.raises(MozbitbarProjectException):
            BitbarProject(project_status)


# Create project #


@pytest.mark.parametrize('kwargs,expected', [
    (
        {
            'project_name': 'parametrized_project',
            'project_type': 'parametrized_type'
        },
        {
            'project_name': 'parametrized_project',
            'project_type': 'parametrized_type'
        },
    ),
    (
        {
            'project_name': string.punctuation,
            'project_type': string.lowercase
        },
        {
            'project_name': string.punctuation,
            'project_type': string.lowercase
        }
    ),
    (
        {
            'project_name': 'mock_project',
            'project_type': 'mock_type'
        },
        MozbitbarProjectException
    ),
    (
        {
            'project_name': 'mock_project',
            'project_type': 'mock_type',
            'permit_duplicate': True
        },
        {
            'project_name': 'mock_project',
            'project_type': 'mock_type'
        }
    )
])
def test_bb_project_init_create_new_project(kwargs, expected):
    """Ensures BitbarProject.create_project() is able to create a project if
    the name is unique. Otherwise, the default behavior is raise an exception,
    unless the permit_duplicate flag is set.
    """
    if expected is MozbitbarProjectException:
        with pytest.raises(MozbitbarProjectException):
            project = BitbarProject('new', **kwargs)
    else:
        project = BitbarProject('new', **kwargs)
        assert project.project_id is not None
        assert project.project_name == expected['project_name']
        assert project.project_type == expected['project_type']


def test_bb_project_create(initialize_project):
    kwargs = {
        'project_name': 'mock_test',
        'project_type': 'mock_type'
    }
    with pytest.raises(MozbitbarProjectException):
        with mock.patch.object(Bitbar,
                               'create_project',
                               side_effect=RequestResponseError(
                                    msg='mock_error', status_code=400)):
            initialize_project.create_project(**kwargs)


# Project ID Property #


@pytest.mark.parametrize('project_id,expected', [
    (1, 1),
    ('1', ValueError),
    (-1, -1),
    ({}, ValueError)
])
def test_bb_project_id(initialize_project, project_id, expected):
    if expected == ValueError:
        with pytest.raises(expected):
            initialize_project.project_id = project_id
    else:
        initialize_project.project_id = project_id
        assert initialize_project.project_id == expected


# Other methods #


def test_get_user_id(initialize_project):
    output = initialize_project.get_user_id()
    assert output
    assert type(output) == int
