from __future__ import print_function, absolute_import

import os

from testdroid import RequestResponseError
from mozbitbar import NotInitializedException
from mozbitbar.bitbar import Bitbar

class BitbarProject(Bitbar):
    """BitbarProject is a class which represents an instance of a project on Bitbar,
    as well as associated actions that require a project id.
    """
    def __init__(self, **kwargs):
        """Initializes the BitbarProject class instance.

        Two methods are currently supported:
            - new project
            - use existing project
        """
        super(BitbarProject, self).__init__()

        if kwargs.get('project_name'):
            self.create_project(**kwargs)
        elif kwargs.get('project_id'):
            self.use_existing_project(kwargs.get('project_id'))
        else:
            raise NotImplementedError()

    def create_project(self, project_name, project_type='ANDROID'):
        """Creates a new Bitbar project using provided parameters.
        """
        # mozilla does not permit creation of project with same names.
        try:
            existing_projects = self.client.get_projects()
            for project in existing_projects['data']:
                if project_name == project['name']:
                    raise EnvironmentError
        except RequestResponseError:
            raise EnvironmentError('Testdroid responded with error.')
        except EnvironmentError:
            raise EnvironmentError('Project with same name exists!')

        # send create project call.
        try:
            output = self.client.create_project(project_name, project_type)
        except RequestResponseError:
            raise EnvironmentError('Testdroid responded with error.')

        # ensure project is created.
        assert output['id']

        # if project creation is confirmed, store project related parameters.
        self.project_name = project_name
        self.project_type = project_type
        self.project_id = output['id']

    def use_existing_project(self, project_id):
        """Use existing Bitbar project.

        This method is simply a wrapper around the set_project_id method,
        which can be used for non-initialization situations.
        """
        self.set_project_id(project_id)

    def set_project_id(self, project_id):
        """Overwrites the self.project_id value with provided project_id.

        Basic checks are performed prior to the overwrite. If any checks
        fail, the task is aborted.
        """
        try:
            output = self.client.get_project(project_id)
        except RequestResponseError:
            raise EnvironmentError('Testdroid responded with error.')

        assert output['id']

        self.project_id = project_id

    def get_project_id(self):
        """Returns the currently assigned project_id value.
        """
        return self.project_id

    def upload_data_file(self, filename):
        """Uploads data file specified using filename parameter.

        This method is a wrapper around the Testdroid implementation.
        """
        if os.path.exists(filename):
            return self.client.upload_test_file(self.project_id, filename)
        else:
            # submit fix to Testdroid to do error handling in upload()
            raise EnvironmentError()

    def start_test_run(self, **kwargs):
        """Starts a test run against a project.

        This method is a wrapper around the Testdroid implementation.
        """
        self.client.start_test_run(self.project_id, **kwargs)
