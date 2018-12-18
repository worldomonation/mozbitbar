from __future__ import print_function, absolute_import

import string

import pytest

from mozbitbar.bitbar_project import BitbarProject
from mozbitbar import ProjectException, FrameworkException


@pytest.fixture()
def initialize_project():
    return BitbarProject('existing', **{'project_name': 'mock_project'})

# Existing projects #

@pytest.mark.parametrize('kwargs,expected', [
    ({'project_id': 11}, {'id': 11}),
    ({'project_id': 99}, {'id': 99}),
    ({'project_id': 100}, ProjectException),
    ({'project_id': 2**32}, ProjectException),
    ({'project_id': -1}, ProjectException),
    (
        {'project_name': 'mock_project'},
        {'name': 'mock_project', 'id': 1}
    ),
    (
        {'project_name': 'another_mock_project'},
        {'name': 'another_mock_project', 'id': 99}
    ),
    ({'project_name': string.lowercase}, ProjectException),
    ({'project_name': 'NULL'}, ProjectException),
    ({'project_name': 'None'}, ProjectException),
])
def test_bb_project_existing(kwargs, expected):
    """Ensures BitbarProject is able to retrieve existing project by id
    or name, and process resulting output of the (mockes) call.

    Directly tests methods involved in:
        - initialization of project
        - retrieve and set project parameters by id or name
    """
    if expected is ProjectException:
        with pytest.raises(ProjectException):
            BitbarProject('existing', **kwargs)

    else:
        project = BitbarProject('existing', **kwargs)
        assert (
            project.project_id == expected.get('id') or
            project.project_name == expected.get('name')
        )


@pytest.mark.parametrize('kwargs,expected', [
    (
        {'project_id': 11, 'project_name': 'mock_project'},
        {'project_id': 11, 'project_name': 'mock_project'}
    ),
    (
        {'project_id': 10000, 'project_name': 'mock_project'},
        {'project_id': 10000, 'project_name': 'yet_another_mock_project'}
    ),
])
def test_bb_project_existing_id_and_name(kwargs, expected):
    """Ensures BitbarProject can accept scenario with both
    id and name provided. Verifies that existing project selection
    prioritizes project id over name.
    """
    project = BitbarProject('existing', **kwargs)
    assert project.project_id == expected['project_id']
    assert project.project_name == expected['project_name']


# Project status #

@pytest.mark.parametrize('project_status,expected', [
    ('present', ProjectException),
    ('exist', ProjectException),
    ('create', ProjectException),
])
def test_bb_project_status(project_status, expected):
    """Ensures BitbarProject raises an exception on invalid project status.
    """
    if expected is ProjectException:
        with pytest.raises(ProjectException):
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
        ProjectException
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
def test_bb_project_create_unique_name(kwargs, expected):
    """Ensures BitbarProject.create_project() is able to create a project if
    the name is unique. Otherwise, the default behavior is raise an exception,
    unless the permit_duplicate flag is set.
    """
    if expected is ProjectException:
        with pytest.raises(ProjectException):
            project = BitbarProject('new', **kwargs)
    else:
        project = BitbarProject('new', **kwargs)
        assert project.project_id is not None
        assert project.project_name == expected['project_name']
        assert project.project_type == expected['project_type']

# Project Framework #

@pytest.mark.parametrize('kwargs,expected', [
    ({'framework_id': 12}, FrameworkException),
    (
        {'framework_id': 1},
        {'framework_name': 'mock_framework', 'framework_id': 1}
    ),
    ({'framework_name': 'mock_framework'}, {
     'framework_name': 'mock_framework', 'framework_id': 1}),
    ({'framework_name': 'mock_framework', 'framework_id': 1}, {
     'framework_name': 'mock_framework', 'framework_id': 1}),
    ({'framework_name': u'mock_framework', 'framework_id': 1}, {
     'framework_name': 'mock_framework', 'framework_id': 1}),
    ({'framework_name': 'mock_unicode_framework'},
     {'framework_name': 'mock_unicode_framework', 'framework_id': 2}),
])
def test_bb_project_framework(initialize_project, kwargs, expected):
    if expected == FrameworkException:
        with pytest.raises(FrameworkException):
            initialize_project.set_project_framework(**kwargs)
    else:
        initialize_project.set_project_framework(**kwargs)
        assert initialize_project.framework_id == expected['framework_id']
        assert initialize_project.framework_name == expected['framework_name']

# Project config #

@pytest.mark.parametrize('kwargs,expected', [
    (
        {'timeout': 10},
        {'timeout': 10}
    ),
    (
        {'timeout': 10, 'scheduler': 'SINGLE'},
        {'timeout': 10, 'scheduler': 'SINGLE'}
    ),
    (
        'not_a_dict', ProjectException
    )
])
def test_set_project_config(initialize_project, kwargs, expected):
    if expected is ProjectException:
        with pytest.raises(ProjectException):
            initialize_project.set_project_configs(new_config=kwargs)
    else:
        initialize_project.set_project_configs(new_config=kwargs)



