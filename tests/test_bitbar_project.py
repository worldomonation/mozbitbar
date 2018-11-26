from __future__ import print_function, absolute_import

import pytest

from mozbitbar.bitbar_project import BitbarProject


def test_bitbar_project_invalid_status():
    with pytest.raises(NotImplementedError):
        BitbarProject(project_status='unknown')


def test_bitbar_project():
    project = BitbarProject('existing', **{'project_id': 000000})
    assert project.project_id == 000000


# @pytest.mark.parametrize(
#     'project_status', 'expected', [('existing', )])
# def test_bitbar_project_status():
