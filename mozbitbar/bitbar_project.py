from __future__ import print_function, absolute_import

import logging
import os

from testdroid import RequestResponseError
from mozbitbar import DataFileException, FrameworkException, ProjectException
from mozbitbar.bitbar import Bitbar

log = logging.getLogger('mozbitbar')

class BitbarProject(Bitbar):
    """BitbarProject is a class which represents an instance of a project on Bitbar,
    as well as associated actions that are intended to be run against a specific project.

    This class holds attributes that are not tracked in the Testdroid implementation relating
    to the project, device groups and/or test runs.
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

    # Class attributes #

    @property
    def project_id(self):
        return self.__project_id

    @project_id.setter
    def project_id(self, project_id):
        if type(project_id) is not int:
            raise ValueError('{}: invalid project_id type provided: expected int, received {}'.format(
                __name__, type(project_id)))
        self.__project_id = project_id

    @property
    def project_name(self):
        return self.__project_name

    @project_name.setter
    def project_name(self, project_name):
        self.__project_name = project_name

    @property
    def project_type(self):
        return self.__project_type

    @project_type.setter
    def project_type(self, project_type):
        self.__project_type = project_type

    @property
    def device_group_id(self):
        return self.__device_group_id

    @device_group_id.setter
    def device_group_id(self, device_group_id):
        if type(device_group_id) is not int:
            raise ValueError('{}: invalid device_group_id type provided: expected int, received {}'.format(
                __name__, type(device_group_id)))
        self.__device_group_id = device_group_id

    def get_user_id(self):
        """Retrieves the user id for the currently authenticated user.

        This method is a wrapper around the Testdroid implementation.

        Returns:
            int: currently authenticated user id.

        Raises:
            RequestResponseError
        """
        return self.client.get_me()['id']

    # Additional methods #

    def _set_project_attributes(self, response):
        """Sets class attributes.

        The following values are set:
            - project_id
            - project_name
            - project_type
        """
        self.project_id = response['id']
        self.project_name = response['name']
        self.project_type = response['type']

    def _is_file_on_bitbar(self, filename):
        """Checks if file with same name has been uploaded to Bitbar for the user.
        """
        # sanitize the provided path to just the file name itself.
        filename = os.path.basename(filename)

        try:
            output = self.client.get_input_files()
            file_names = [file_list['name'] for file_list in output['data']]
        except RequestResponseError as rre:
            raise rre

        return filename in file_names

    # Project operations #

    def create_project(self, **kwargs):
        """Creates a new Bitbar project using provided parameters.
        """
        project_name = kwargs.get('project_name')
        project_type = kwargs.get('project_type')

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
        output = self.client.create_project(project_name, project_type)

        # ensure project is created.
        assert output['id']

        # if project creation is confirmed, store project related parameters.
        self._set_project_attributes(output)

    def use_existing_project(self, **kwargs):
        """Use existing Bitbar project to set project parameters.

        This method is a wrapper that calls the appropriate methods depending on
        provided parameters.
        """
        if kwargs.get('project_id'):
            self.set_project_by_id(kwargs.get('project_id'))
        if kwargs.get('project_name'):
            self.set_project_by_name(kwargs.get('project_name'))

    def set_project_by_id(self, project_id):
        """Retrieves project parameters from Bitbar using project_id.
        """
        output = self.client.get_project(project_id)

        try:
            assert project_id in output
        except AssertionError:
            raise ProjectException('Project with id: {} not found.'.format(project_id))

        self._set_project_attributes(output)

    def set_project_by_name(self, project_name):
        """Retrieves project parameters from Bitbar using project_name.
        """
        try:
            output = self.client.get_projects()
        except RequestResponseError:
            raise EnvironmentError('Testdroid responded with error.')

        for project in output['data']:
            if project_name == project['name']:
                self._set_project_attributes(project)

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
        output = self.client.get_frameworks()
        return [(framework['name'], framework['id']) for framework in output['data']]

    def set_project_config(self, config):
        self.client.set_project_config(self.project_id, config)
        pass

    def set_project_parameters(self, parameters):
        assert type(parameters) is dict

        self.client.set_project_parameters(self.project_id, parameters)
        pass

    # File operations #

    def upload_file(self, **kwargs):
        """Uploads file(s) to Bitbar.

        Supports upload of multiple files, of all types supported by Bitbar.
        """
        for key, filename in kwargs.iteritems():
            file_type, _ = key.split('_')
            path = "users/{user_id}/projects/{project_id}/files/{file_type}".format(user_id=self.get_user_id(), project_id=self.project_id, file_type=file_type)
            output = self.client.upload(path=path, filename=filename)
            assert output

            try:
                assert self._is_file_on_bitbar(filename)
            except AssertionError:
                raise DataFileException("Data file {} could not be uploaded to Bitbar.".format(filename))

    # Device operations #

    def set_device_group(self, specified_device_group):
        """Sets the project's device group to be used for test runs.
        """
        device_groups = [(device_group['id'], device_group['name'])
                         for device_group in self.client.get_device_groups()['data']]

        # if device_group_name is provided, the device_group_id must be retrieved using the name.
        if type(specified_device_group) is str:
            for device_group in device_groups:
                if specified_device_group in device_group:
                    specified_device_group = device_group[1]

        self.device_group_id = specified_device_group

    # Test Run operations #

    def start_test_run(self, **kwargs):
        """Starts a test run with parameters based on recipe definition.

        This method is a wrapper around the Testdroid implementation with
        additional operations.
        """
        if kwargs.get('device_group_id') or kwargs.get('device_group_name'):
            self.set_device_group(kwargs.pop('device_group_id') or kwargs.pop('device_group_name'))

        from datetime import datetime
        self.client.start_test_run(self.project_id, device_group_id=self.device_group_id, name='yaml test', **kwargs)
