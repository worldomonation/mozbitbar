from __future__ import print_function, absolute_import

import os

from testdroid import RequestResponseError
from mozbitbar import NotInitializedException, DataFileException, FrameworkException
from mozbitbar.bitbar import Bitbar

class BitbarProject(Bitbar):
    """BitbarProject is a class which represents an instance of a project on Bitbar,
    as well as associated actions that require a project id.
    """
    def __init__(self, project_status, **kwargs):
        """Initializes the BitbarProject class instance.

        Two methods are currently supported:
            - new project
            - use existing project
        """
        super(BitbarProject, self).__init__()

        if 'new' in project_status:
            self.create_project(**kwargs)
        elif 'existing' in project_status:
            self.use_existing_project(**kwargs)
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
        self._set_project_parameters_from_response(output)

    def _set_project_parameters_from_response(self, response):
        """Sets necessary project parameters given a dictionary.

        The following values are set:
            - project_id
            - project_name
            - project_type
        """
        self.project_id = response['id']
        self.project_name = response['name']
        self.project_type = response['type']

    def use_existing_project(self, **kwargs):
        """Use existing Bitbar project to set project parameters.

        This method is a wrapper that calls the appropriate methods depending on
        provided parameters.
        """
        print(kwargs.get('project_id'))
        if kwargs.get('project_id'):
            self.set_project_id(kwargs.get('project_id'))
        if kwargs.get('project_name'):
            self.set_project_name(kwargs.get('project_name'))

    def set_project_id(self, project_id):
        """Retrieves project parameters from Bitbar using project_id.
        """
        try:
            output = self.client.get_project(project_id)
        except RequestResponseError:
            raise EnvironmentError('Testdroid responded with error.')

        assert output

        self._set_project_parameters_from_response(output)

    def set_project_name(self, project_name):
        """Retrieves project parameters from Bitbar using project_name.
        """
        try:
            output = self.client.get_projects()
        except RequestResponseError:
            raise EnvironmentError('Testdroid responded with error.')

        for project in output['data']:
            if project_name == project['name']:
                self._set_project_parameters_from_response(project)

        if not self.project_id:
            raise EnvironmentError('Project with name {} not found.'.format(project_name))

    def set_project_framework(self, **kwargs):
        """Sets the project framework using either integer id or name.

        This method prioritizes framework name if both are provided.
        """
        framework_list = self.get_project_frameworks()
        framework_to_use = kwargs.get('framework_name') or kwargs.get('frameworkId')

        for framework in framework_list:
            if framework_to_use in framework:
                framework_id = framework[1]

        if not framework_id:
            raise NotImplementedError(
                'Invalid framework identifer provided: {}'.format(kwargs.values()))

        try:
            self.client.set_project_framework(self.project_id, framework_id)
        except RequestResponseError:
            raise EnvironmentError('Testdroid responded with error.')

    def get_project_frameworks(self):
        """Returns list of project frameworks available to the user.
        """
        try:
            output = self.client.get_frameworks()
            return [(framework['name'], framework['id']) for framework in output['data']]
        except RequestResponseError:
            raise EnvironmentError('Testdroid responded with error.')

    def get_project_id(self):
        """Returns the currently assigned project_id value.
        """
        return self.project_id

    def _is_file_on_bitbar(self, filename):
        """Checks if the file is already uploaded to Bitbar.
        """
        # sanitize the provided path to just the file name itself.
        filename = os.path.basename(filename)

        try:
            output = self.client.get_input_files()
            file_names = [file_list['name'] for file_list in output['data']]
        except RequestResponseError as rre:
            raise rre

        if filename in file_names:
            return True
        return False

    def upload_data_file(self, filename):
        """Uploads data file specified using filename parameter.

        This method is a wrapper around the Testdroid implementation, with additional
        checks performed.
        """
        if not self._is_file_on_bitbar(filename):
            if os.path.exists(filename):
                try:
                    self.client.upload_data_file(self.project_id, filename)
                except RequestResponseError as e:
                    raise e

                try:
                    assert self._is_file_on_bitbar(filename)
                except AssertionError:
                    raise DataFileException("Data file {} could not be uploaded to Bitbar.".format(filename))
            else:
                # submit fix to Testdroid to do error handling in upload(), so we don't need to handle that scenario here.
                raise EnvironmentError()
        raise DataFileException("Data file with same name '{}' is already on Bitbar.".format(filename))

    def start_test_run(self, **kwargs):
        """Starts a test run against a project.

        This method is a wrapper around the Testdroid implementation.
        """
        self.client.start_test_run(self.project_id, **kwargs)
