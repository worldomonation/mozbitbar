from __future__ import print_function, absolute_import

import pytest

from mozbitbar.bitbar_project import BitbarProject
from mozbitbar import ProjectException


@pytest.mark.parametrize('kwargs,expected', [
        ({'project_id': 1}, 1),
        ({'project_id': 999}, 999),
        ({'project_id': 2**32}, 2**32),
        ({'project_id': 0}, 0),
        ({'project_id': -1}, -1),
        ])
def test_bitbar_project(kwargs, expected):
    """Ensures BitbarProject sets project_id as expected.

    Directly tests methods involved in:
        - initialization
        - branching logic based on project_id or project_name
        - setting of project by project_id

    Indirectly tests methods involved in:
        - property setter for project_id

    Last call Testdroid.get_project is mocked.
    """
    project = BitbarProject('existing', **kwargs)
    assert project.project_id == expected


@pytest.mark.parametrize('project_status', ['present', 'exist', 'create'])
def test_bitbar_project_invalid_status(project_status):
    """Ensures BitbarProject raises an exception on invalid project status.
    """
    with pytest.raises(ProjectException):
        BitbarProject(project_status)
