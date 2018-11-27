from __future__ import print_function, absolute_import

import logging
import os

from testdroid import RequestResponseError
from mozbitbar import FileException, FrameworkException, ProjectException
from mozbitbar.bitbar import Bitbar


class BitbarProject(Bitbar):
    """BitbarProject is a class which represents an instance of a project on Bitbar,
    as well as associated actions that are intended to be run against a specific project.

    This class holds attributes that are not tracked in the Testdroid implementation relating
    to the project, device groups and/or test runs.
    """
    def __init__(self, project_status, **kwargs):
        """Initializes the BitbarProject class instance.

        Two methods of are currently supported:
            - new project ('new')
            - use of existing project ('existing')

        If a new project is specified, project_type and project_name attributes must be provided.

        If an existing project is specified, at minimum the project_name or project_id must be specified.

        Args:
            project_status (str): Expected to be 'new' or 'existing'. Raises an exception on any other input.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            ProjectException: If `project_status` has value other than 'new' or 'existing'.
        """
        super(BitbarProject, self).__init__()

        if 'new' in project_status:
            self.create_project(**kwargs)
        elif 'existing' in project_status:
            self.use_existing_project(**kwargs)
        else:
            raise ProjectException('invalid project status specifier received, project cannot be set.' + '\nproject status: {}'.format(project_status))

    # Class attributes #

    @property
    def project_id(self):
        """Returns the project_id attribute.

        When setting the project_id, checks are performed to ensure the value is an integer.

        Args:
            project_id (int): Value to set for the project_id attribute of this object.

        Raises:
            ValueError: If project_id is not of type int.
        """
        return self.__project_id

    @project_id.setter
    def project_id(self, project_id):
        if type(project_id) is not int:
            raise ValueError('{}: invalid project_id type provided: expected int, received {}'.format(
                __name__, type(project_id)))
        self.__project_id = project_id

    @property
    def project_name(self):
        """Returns the project_name attribute.

        Args:
            project_name (str): Value to set for the project_name attribute of this object.
        """
        return self.__project_name

    @project_name.setter
    def project_name(self, project_name):
        self.__project_name = project_name

    @property
    def project_type(self):
        """Returns the project_type attribute.

        Args:
            project_type (str): Value to set for the project_type attribute of this object.
        """
        return self.__project_type

    @project_type.setter
    def project_type(self, project_type):
        self.__project_type = project_type

    @property
    def device_group_id(self):
        """Returns the device_group_id attribute.

        Args:
            device_group_id (int): Value to set for the device_group_id attribute of this object.

        Raises:
            ValueError: If device_group_id is not of type int.
        """
        return self.__device_group_id

    @device_group_id.setter
    def device_group_id(self, device_group_id):
        if type(device_group_id) is not int:
            raise ValueError('{}: invalid device_group_id type provided: expected int, received {}'.format(
                __name__, type(device_group_id)))
        self.__device_group_id = device_group_id

    @property
    def framework_id(self):
        """Returns the framework_id attribute.

        Args:
            framework_id (int): Value to set for the framework_id attribute of this object.
        """
        return self.__framework_id

    @framework_id.setter
    def framework_id(self, framework_id):
        self.__framework_id = framework_id

    def get_user_id(self):
        """Retrieves the user id for the currently authenticated user.

        This method is a wrapper around the Testdroid implementation.

        Returns:
            int: currently authenticated user id.

        Raises:
            RequestResponseError: If Testdroid is unable to make requests.
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
        if 'project_id' in kwargs.keys():
            self.set_project_by_id(kwargs.get('project_id'))
        if 'project_name' in kwargs.keys():
            self.set_project_by_name(kwargs.get('project_name'))

    def set_project_by_id(self, project_id):
        """Retrieves project parameters from Bitbar using project_id.
        """
        output = self.client.get_project(project_id)

        try:
            assert project_id in output.values()
        except AssertionError:
            raise ProjectException('Project with id: {} not found.'.format(project_id))

        self._set_project_attributes(output)

    def set_project_by_name(self, project_name):
        """Retrieves project parameters from Bitbar using project_name.
        """
        output = self.client.get_projects()

        for project in output['data']:
            if project_name == project['name']:
                self._set_project_attributes(project)

        if not self.project_id:
            raise ProjectException(
                'Project with name {} not found.'.format(project_name))

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

    def set_project_parameters(self, parameters, force_overwrite=False):
        """Sets project parameters.

        Will accept any number of parameters in the form of a list.
        """
        if not parameters:
            print('No project parameters supplied.')
            return

        if force_overwrite:
            for parameter in parameters:
                # delete existing project parameters that match the key values
                # in 'parameters' argument.
                self.delete_project_parameter(parameter['key'])

        for parameter in parameters:
            try:
                output = self.client.set_project_parameters(self.project_id, parameter)
                assert output['id']
            except RequestResponseError as rre:
                if rre.status_code is 409:
                    print(rre.message, 'skipping..')

    def delete_project_parameter(self, parameter_to_delete):
        """Deletes a single project parameter from the project.

        Given a single instance of a project parameter, this method will
        attempt to delete the project parameter.
        """
        try:
            sanitized_parameter_id = int(parameter_to_delete)
        except ValueError:
            sanitized_parameter_id = self.get_project_parameter_id_by_name(
                parameter_to_delete)

        if sanitized_parameter_id is None:
            print('Parameter to delete {} not found, skipping..'.format(parameter_to_delete))
            return

        assert type(sanitized_parameter_id) is int

        output = self.client.delete_project_parameters(self.project_id, sanitized_parameter_id)
        assert output.status_code is 204

    def get_project_parameter_id_by_name(self, parameter_name):
        """Returns the parameter_id value represented by the string.

        This method will convert the string representation of the project parameter name to
        an integer id.
        """
        assert type(parameter_name) is str

        output = self.client.get_project_parameters(self.project_id)
        for parameter in output['data']:
            if parameter_name == parameter['key']:
                return parameter['id']

        return None

    # File operations #

    def _file_on_local_disk(self, path):
        """checks if specified path can be found on local disk.
        """
        assert type(path) == str

        absolute_path = os.path.abspath(path)
        return os.path.isfile(absolute_path)

    def _file_on_bitbar(self, filename):
        """Checks if file with same name has been uploaded to Bitbar for the user.
        """
        assert type(filename) == str
        # sanitize the provided path to just the file name itself.
        filename = os.path.basename(filename)

        output = self.client.get_input_files()
        file_names = [file_list['name'] for file_list in output['data']]

        return filename in file_names

    def upload_file(self, **kwargs):
        """Uploads file(s) to Bitbar.

        Supports upload of multiple files, of all types supported by Bitbar.
        """
        for key, filename in kwargs.iteritems():
            file_type, _ = key.split('_')

            if self._file_on_bitbar(filename):
                print('File name: {} already exists on Bitbar, skipping.'.format(filename))
                continue

            try:
                assert self._file_on_local_disk(filename)
            except AssertionError:
                raise FileException('Failed to locate file on disk: path: {}'.format(filename))

            api_path = "users/{user_id}/projects/{project_id}/files/{file_type}".format(
                user_id=self.get_user_id(), project_id=self.project_id, file_type=file_type)
            output = self.client.upload(path=api_path, filename=filename)

            assert output

            try:
                assert self._file_on_bitbar(filename)
            except AssertionError:
                raise FileException("Failed to upload file to Bitbar: file type: {}, file name: {}".format(file_type, filename))

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

        self.client.start_test_run(self.project_id, device_group_id=self.device_group_id, name='yaml test', **kwargs)
