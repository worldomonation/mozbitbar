from __future__ import print_function, absolute_import

import os

from testdroid import RequestResponseError
from mozbitbar import FileException, ProjectException, FrameworkException
from mozbitbar.bitbar import Bitbar


class BitbarProject(Bitbar):
    """BitbarProject is a class which represents an instance of a project on
    Bitbar, as well as associated actions that are intended to be run against
    a specific project.

    This class holds attributes that are not tracked in the Testdroid
    implementation relating to the project, device groups and/or test runs.
    """
    def __init__(self, project_status, **kwargs):
        """Initializes the BitbarProject class instance.

        Two methods of are currently supported:
            - new project ('new')
            - use of existing project ('existing')

        If a new project is specified, project_type and project_name attributes
        must be provided.

        If an existing project is specified, at minimum the project_name or
        project_id must be specified.

        Args:
            project_status (str): Expected to be 'new' or 'existing'.
                Raises an exception on any other input.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            ProjectException: If `project_status` has value other than 'new'
                or 'existing'.
        """
        super(BitbarProject, self).__init__()

        if 'new' in project_status:
            self.create_project(**kwargs)
        elif 'existing' in project_status:
            self.use_existing_project(**kwargs)
        else:
            raise ProjectException('invalid project status specifier ' +
                                   'received, project cannot be set.' +
                                   '\nproject status: {}'.format(
                                       project_status))

    # Class attributes #

    @property
    def project_id(self):
        """Returns the project_id attribute.

        When setting the project_id, checks are performed to ensure the value
        is an integer.

        Args:
            project_id (int): Value to set for the project_id attribute
            of this object.

        Raises:
            ValueError: If project_id is not of type int.
        """
        return self.__project_id

    @project_id.setter
    def project_id(self, project_id):
        if type(project_id) is not int:
            raise ValueError('{}: invalid project_id type:'.format(__name__) +
                             'expected int, received {}'.format(
                                 type(project_id)))
        self.__project_id = project_id

    @property
    def project_name(self):
        """Returns the project_name attribute.

        Args:
            project_name (str): Value to set for the project_name attribute
            of this object.
        """
        return self.__project_name

    @project_name.setter
    def project_name(self, project_name):
        self.__project_name = project_name

    @property
    def project_type(self):
        """Returns the project_type attribute.

        Args:
            project_type (str): Value to set for the project_type attribute
            of this object.
        """
        return self.__project_type

    @project_type.setter
    def project_type(self, project_type):
        self.__project_type = project_type

    @property
    def device_group_id(self):
        """Returns the device_group_id attribute.

        Args:
            device_group_id (int): Value to set for the device_group_id
            attribute of this object.

        Raises:
            ValueError: If device_group_id is not of type int.
        """
        return self.__device_group_id

    @device_group_id.setter
    def device_group_id(self, device_group_id):
        if type(device_group_id) is not int:
            raise ValueError('invalid device_group_id type:' +
                             'expected int, received {}'.format(
                                type(device_group_id)))
        self.__device_group_id = device_group_id

    @property
    def framework_id(self):
        """Returns the framework_id attribute.

        Args:
            framework_id (int): Value to set for the framework_id attribute
            of this object.
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
            RequestResponseError: If Testdroid responds with an error.
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

    def get_projects(self):
        """Returns the list of projects.

        Returns:
            dict: Contains data on projects available on Bitbar.
        """
        existing_projects = self.client.get_projects()
        return existing_projects['data']

    # Project operations #

    def create_project(self, **kwargs):
        """Creates a new Bitbar project using provided parameters.

        Args:
            **kwargs: Arbitrary keyword arguments.
        """
        project_name = kwargs.get('project_name')
        project_type = kwargs.get('project_type')

        # first, check if project with same name already exists.
        # this is a constraint imposed by Mozilla.
        try:
            existing_projects = self.get_projects()
            for project in existing_projects:
                if project_name == project['name']:
                    raise ProjectException
        except ProjectException:
            raise ProjectException('Project with same name exists.')

        output = self.client.create_project(project_name, project_type)
        assert output['id']
        self._set_project_attributes(output)

    def use_existing_project(self, **kwargs):
        """Use existing Bitbar project to set project parameters.

        This method is a wrapper that calls the appropriate methods depending
        on provided parameters.

        Args:
            **kwargs: Arbitrary keyword arguments.
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
            raise ProjectException('Project with id: {} not found.'.format(
                                   project_id))

        self._set_project_attributes(output)

    def set_project_by_name(self, project_name):
        """Retrieves project parameters from Bitbar using project_name.

        Args:
            project_name (str): Project name to use in order to set project
                attributes if found.

        Raises:
            ProjectException: If project_name is not found in the list of
                available projects on Bitbar.
            RequestResponseError: If Testdroid responds with an error.
        """
        available_projects = self.get_projects()

        for project in available_projects:
            if project_name == project['name']:
                self._set_project_attributes(project)

        if not self.project_id:
            raise ProjectException(
                'Project with name {} not found.'.format(project_name))

    def set_project_framework(self, **kwargs):
        """Sets the project framework using either integer id or name.

        This method prioritizes framework name if both id and name are
        provided.

        If a framework name or id is provided that is not available on
        Bitbar, a FrameworkException is raised.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Raises:
            FrameworkException: If framework name or framework id provided
                does not match any existing frameworks on Bitbar.
            RequestResponseError: If Testdroid responds with an error.
        """
        available_frameworks = self.get_project_frameworks()
        framework_to_set = (kwargs.get('framework_name') or
                            kwargs.get('frameworkId'))

        for framework in available_frameworks:
            if framework_to_set in framework:
                framework_id = framework[1]

        if not framework_id:
            raise FrameworkException(
                'Invalid framework identifer provided: {}'.format(
                    kwargs.values()))

        self.client.set_project_framework(self.project_id, framework_id)

    def get_project_frameworks(self):
        """Returns list of project frameworks available to the user.

        Returns:
            :obj:`list` of :obj:`tuple`: of :obj:`str`
        """
        output = self.client.get_frameworks()
        return [(framework['name'], framework['id'])
                for framework in output['data']]

    def set_project_parameters(self, parameters, force_overwrite=False):
        """Sets project parameters.

        Will accept any number of parameters in the form of a list.

        If specified parameter is already set, the default behavior is to
        retain existing parameter, moving to the next specified parameter.

        If the force_overwrite flag is supplied, all existing parameters
        that match list of supplied parameters are first removed from
        the project. The parameters are then set from the list of supplied
        parameters as normal, in effect overwriting the parameter values.

        Args:
            parameters (:obj:`list` of :obj:`dict`): List of project parameters
                to be set for the current project.
            force_overwrite (bool, optional): True if project parameters are
                to be overwritten. False by default.

        Raises:
            RequestResponseError: If Testdroid responds with an error.
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
                output = self.client.set_project_parameters(self.project_id,
                                                            parameter)
                assert output['id']
            except RequestResponseError as rre:
                if rre.status_code is 409:
                    print(rre.message, 'skipping..')

    def delete_project_parameter(self, parameter_to_delete):
        """Deletes a single project parameter from the project.

        Given a single instance of a project parameter, this method will
        attempt to delete the project parameter from the project.

        Accepts both integer and string representation of the parameter id
        and name, respectively.

        If the parameter to delete is found, an attempt is made using
        Testdroid to delete the said parameter.

        Args:
            parameter_to_delete (str, int): Project parameter to be deleted
                from the project. Could be string (name) or integer (id).

        Raises:
            AssertionError: If HTTPS response of the deletion attempt is
                anything other than 204.
            RequestResponseError: If Testdroid responds with an error.
        """
        try:
            # maybe user supplied a stringified integer value.
            sanitized_parameter_id = int(parameter_to_delete)
        except ValueError:
            # if not, we have a parameter_name that needs conversion to id.
            sanitized_parameter_id = self.get_project_parameter_id_by_name(
                parameter_to_delete)

        if sanitized_parameter_id is None:
            # if user-supplied parameter name or id is not in fact set for the
            # project on Bitbar, skip the deletion process.
            print('Parameter ID for {} not found.'.format(parameter_to_delete),
                  'skipping..')
            return

        assert type(sanitized_parameter_id) is int

        output = self.client.delete_project_parameters(
            self.project_id,
            sanitized_parameter_id
        )
        assert output.status_code is 204

    def get_project_parameter_id_by_name(self, parameter_name):
        """Returns the parameter_id value represented by the string.

        This method will convert the string representation of the
        project parameter name to an integer id.

        Args:
            parameter_name (str): Parameter name in string format, to convert
                to a numerical ID.

        Returns:
            int or None: Integer if parameter name maps to an existing project
                parameter on Bitbar. None otherwise.

        Raises:
            RequestResponseError: If Testdroid responds with an error.
        """
        assert type(parameter_name) is str

        output = self.client.get_project_parameters(self.project_id)
        for parameter in output['data']:
            if parameter_name == parameter['key']:
                return parameter['id']

        return None

    # File operations #

    def _file_on_local_disk(self, path):
        """Checks if specified path can be found on local disk.

        Accepts a string representation of a local path. Firstly, the current
        directory is checked. If path could not be found, the path is
        converted to an absolute path.

        Args:
            path (str): String representation of a path on local disk.

        Returns:
            bool: True if path is found on local disk. False otherwise.
        """
        assert type(path) == str

        if os.path.isfile(path):
            return True

        absolute_path = os.path.abspath(path)
        return os.path.isfile(absolute_path)

    def _file_on_bitbar(self, filename):
        """Checks if file with same name has been uploaded to Bitbar which
        is available to the user.

        Args:
            filename (str): String representation of a filename.

        Returns:
            bool: True if filename is found on Bitbar. False otherwise.
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

        Args:
            **kwargs: Arbitrary keyword arguments.

        Raises:
            FileException: If file could not be uploaded to Bitbar.
        """
        for key, filename in kwargs.iteritems():
            file_type, _ = key.split('_')

            if self._file_on_bitbar(filename):
                # skip and go to the next item in the list of files.
                print('File name: {} already exists on Bitbar,' +
                      'skipping.'.format(filename))
                continue

            try:
                assert self._file_on_local_disk(filename)
            except AssertionError:
                raise FileException('Failed to locate file on disk: path: ' +
                                    '{}'.format(filename))

            api_path_components = [
                "users/{user_id}/".format(user_id=self.get_user_id()),
                "projects/{project_id}/".format(project_id=self.project_id),
                "files/{file_type}".format(file_type=file_type)
            ]
            api_path = ''.join([api_path_components])

            output = self.client.upload(path=api_path, filename=filename)

            assert output

            try:
                assert self._file_on_bitbar(filename)
            except AssertionError:
                raise FileException('Failed to upload file to Bitbar: ' +
                                    'file type: {}, '.format(file_type) +
                                    'file name: {}'.format(filename))

    # Device operations #

    def get_device_groups(self):
        """Returns the list of device groups available on Bitbar.

        Returns:
            :obj:`list` of :obj:`dict`: List of currently available device
                groups.

        Raises:
            RequestResponseError: If Testdroid responds with an error.
        """
        return self.client.get_device_groups()['data']

    def set_device_group(self, device_group_to_set):
        """Sets the project's device group to be used for test runs.

        Args:
            device_group_to_set (str, int): Device group specifier to be
                used to set the device group. Could be string
                (device group name) or integer (device group id).
        """
        device_groups = [(device_group['id'], device_group['name'])
                         for device_group in self.get_device_groups()]

        # if device_group_name is provided, the device_group_id must be
        # retrieved using the name.
        if type(device_group_to_set) is str:
            for device_group in device_groups:
                if device_group_to_set in device_group:
                    device_group_to_set = device_group[1]

        assert type(device_group_to_set) is int

        self.device_group_id = device_group_to_set

    # Test Run operations #

    def start_test_run(self, **kwargs):
        """Starts a test run with parameters provided from the recipe.

        This method is a wrapper around the Testdroid implementation with
        additional operations.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            int: Unique test run ID generated by Bitbar.

        Raises:
            RequestResponseError: If Testdroid responds with an error.
        """
        if kwargs.get('device_group_id') or kwargs.get('device_group_name'):
            self.set_device_group(kwargs.pop('device_group_id') or
                                  kwargs.pop('device_group_name'))

        self.client.start_test_run(self.project_id,
                                   device_group_id=self.device_group_id,
                                   name='yaml test', **kwargs)
