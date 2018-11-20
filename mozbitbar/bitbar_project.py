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
        elif kwargs.get('project_name'):
            self.use_existing_project(kwargs.get('project_name'))
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
        self._set_project_parameters(output)

    def _set_project_parameters(self, data):
        """Sets necessary project parameters given a dictionary.

        The following values are set:
            - project_id
            - project_name
            - project_type
        """
        self.project_id = data['id']
        self.project_name = data['name']
        self.project_type = data['type']

    def use_existing_project(self, identifier):
        """Use existing Bitbar project to set project parameters.

        This method is a wrapper that calls the appropriate methods depending on
        provided parameters.
        """
        if type(identifier) == int:
            self.set_project_id(identifier)
        if type(identifier) == str:
            self.set_project_name(identifier)

    def set_project_id(self, project_id):
        """Sets the project parameters using project_id.
        """
        try:
            output = self.client.get_project(project_id)
        except RequestResponseError:
            raise EnvironmentError('Testdroid responded with error.')

        assert output

        self._set_project_parameters(output)

    def set_project_name(self, project_name):
        """Sets the project parameters using project_name.
        """
        try:
            output = self.client.get_projects()
        except RequestResponseError:
            raise EnvironmentError('Testdroid responded with error.')

        for project in output['data']:
            if project_name == project['name']:
                self._set_project_parameters(project)

        if not self.project_id:
            raise EnvironmentError('Project with name {} not found.'.format(project_name))


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
