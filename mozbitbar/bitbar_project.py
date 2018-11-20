from __future__ import print_function, absolute_import

import os

from testdroid import RequestResponseError
from mozbitbar import NotInitializedException
from mozbitbar.bitbar import Bitbar

class BitbarProject(Bitbar):
    """BitbarProject is a class which represents an instance of a project on Bitbar,
    as well as associated actions that require a project id.
    """
    def __init__(self, project_id=None, **kwargs):
        """Initializes the BitbarProject class instance.

        Two methods are currently supported:
            - new project
            - use existing project
        """
        super(BitbarProject, self).__init__()

        if kwargs.get('project_name'):
            self.create_project(**kwargs)
        elif project_id:
            self.set_project_id(project_id)
        else:
            raise NotImplementedError()

    # Project attributes.
    def create_project(self, project_name, project_type='ANDROID'):
        # create a new project
        try:
            output = self.client.create_project(project_name, project_type)
        except RequestResponseError:
            raise EnvironmentError('Testdroid responded with error.')

        # ensure project is created
        assert output['id']

        self.project_name = project_name
        self.project_type = project_type
        self.project_id = output['id']

    def set_project_id(self, project_id):
        try:
            output = self.client.get_project(project_id)
        except RequestResponseError:
            raise EnvironmentError('Testdroid responded with error.')

        assert output['id']

        self.project_id = project_id

    def get_project_id(self):
        return self.project_id

    # File operations
    def upload_data_file(self, filename):
        if os.path.exists(filename):
            return self.client.upload_test_file(self.project_id, filename)
        else:
            # submit fix to Testdroid to do error handling in upload()
            raise EnvironmentError()

    # Test run operations
    def start_test_run(self, **kwargs):
        self.client.start_test_run(self.project_id, **kwargs)
