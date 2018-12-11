from __future__ import print_function, absolute_import

import string

import pytest

from mozbitbar.bitbar_project import BitbarProject
from mozbitbar import ProjectException, FrameworkException


# Project with Existing ID #

@pytest.mark.parametrize('kwargs,expected', [
    ({'id': 1}, 1),
    ({'id': 99}, 99),
    ({'id': 100}, ProjectException),
    ({'id': 2**32}, ProjectException),
    ({'id': -1}, ProjectException),
])
def test_bb_project_existing_by_id(kwargs, expected):
    """Ensures BitbarProject sets id as expected.

    Directly tests methods involved in:
        - initialization
        - setting of project by id

    Indirectly tests methods involved in:
        - property setter for id

    Last call Testdroid.get_project is mocked to return a pseudo
    project.
    """
    if expected is ProjectException:
        with pytest.raises(ProjectException):
            BitbarProject('existing', **kwargs)

    else:
        project = BitbarProject('existing', **kwargs)
        assert project.project_id == expected


@pytest.mark.parametrize('kwargs,expected', [
    ({'name': 'mock_project'}, 'mock_project'),
    ({'name': 'another_mock_project'}, 'another_mock_project'),
    ({'name': string.lowercase}, ProjectException),
    ({'name': 'NULL'}, ProjectException),
    ({'name': 'None'}, ProjectException),
])
def test_bb_project_existing_by_name(kwargs, expected):
    """Ensures BitbarProject sets name as expected.

    Directly tests methods involved in:
        - initialization
        - branching logic based on name or name
        - setting of project by name

    Indirectly tests methods involved in:
        - property setter for name

    Last call Testdroid.get_project is mocked to return a pseudo
    project.
    """
    if expected is ProjectException:
        with pytest.raises(ProjectException):
            BitbarProject('existing', **kwargs)

    else:
        project = BitbarProject('existing', **kwargs)
        assert project.project_name == expected


@pytest.mark.parametrize('kwargs,expected', [
    ({'id': 1, 'name': 'mock_project'}, [1, 'mock_project']),
    ({'id': 10000, 'name': 'mock_project'},
     [10000, 'yet_another_mock_project']),
])
def test_bb_project_existing_id_and_name(kwargs, expected):
    """Ensures BitbarProject can accept scenario with both
    id and name provided. Verifies that existing project selection
    prioritizes project id over name.
    """
    project = BitbarProject('existing', **kwargs)
    assert project.project_id == expected[0]
    assert project.project_name == expected[1]


# Project status method #

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


# Project with New ID #


@pytest.mark.parametrize('kwargs', [
    ({
        'name': 'parametrized_project_1',
        'type': 'parametrized_type'
    }),
    ({
        'name': string.punctuation,
        'type': string.lowercase
    })
])
def test_bb_project_create_unique_name(kwargs):
    """Ensures BitbarProject.create_project() is able to create a valid
    project instance given appropriate project name and type.
    """
    project = BitbarProject('new', **kwargs)
    assert project.project_id is not None
    assert project.project_name == kwargs['project_name']
    assert project.project_type == kwargs['project_type']


@pytest.mark.parametrize('kwargs', [
    ({
        'name': 'mock_project',
        'type': 'mock_type'
    })
])
def test_bb_project_create_duplicate_name_without_flag(kwargs):
    with pytest.raises(ProjectException):
        BitbarProject('new', **kwargs)


@pytest.mark.parametrize('kwargs', [
    ({
        'project_name': 'mock_project',
        'project_type': 'mock_type',
        'permit_duplicate': True,
    })
])
def test_bb_project_create_duplicate_name_with_flag(kwargs):
    pass


@pytest.mark.parametrize('kwargs,expected', [
    ({'id': 12}, FrameworkException),
    ({'id': 1}, {'name': 'mock_framework', 'id': 1}),
    ({'name': 'mock_framework'}, {'name': 'mock_framework', 'id': 1}),
    ({'name': 'mock_framework', 'id': 1}, {'name': 'mock_framework', 'id': 1}),
    ({'name': u'mock_framework', 'id': 1}, {'name': 'mock_framework', 'id': 1}),
    ({'name': 'mock_unicode_framework'},
     {'name': 'mock_unicode_framework', 'id': 2}),
])
def test_bb_project_framework(kwargs, expected):
    project = BitbarProject('existing', **{'id': 99})
    if expected == FrameworkException:
        with pytest.raises(FrameworkException):
            project.set_project_framework(**kwargs)
    else:
        project.set_project_framework(**kwargs)
        assert project.framework_id == expected['id']
        assert project.framework_name == expected['name']
