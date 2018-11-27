from __future__ import print_function, absolute_import

import pytest

from mozbitbar.bitbar_project import BitbarProject
from mozbitbar import ProjectException

@pytest.mark.parametrize('kwargs,expected', [ ({'project_id': 1}, 1) ])
def test_bitbar_project(mock_bitbar_project, kwargs, expected):
    project = mock_bitbar_project('existing', **kwargs)
    assert project.project_id == expected


@pytest.mark.parametrize('project_status', ['present', 'exist', 'create'])
def test_bitbar_project_invalid_status(project_status):
    with pytest.raises(ProjectException):
        BitbarProject(project_status)
