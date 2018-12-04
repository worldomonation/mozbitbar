from __future__ import print_function, absolute_import

import json
import os
import time

from testdroid import RequestResponseError
from mozbitbar import (
    FileException,
    ProjectException,
    FrameworkException,
    DeviceException,
    TestException
)
from mozbitbar.__root__ import path as root_path
from mozbitbar.configuration import Configuration


class BitbarProject(Configuration):
    """BitbarProject is a class which represents an instance of a project on
    Bitbar, as well as associated actions that are intended to be run against
    a specific project instance.

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
            ProjectException: If project_status has value other than 'new'
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
    def device_group_name(self):
        """Returns the device_group_name attribute.

        Args:
            device_group_name (str): Value to set for the device_group_name
            attribute of this object.

        Raises:
            ValueError: If device_group_name is not of type str.
        """
        return self.__device_group_name

    @device_group_name.setter
    def device_group_name(self, device_group_name):
        if type(device_group_name) is not str:
            raise ValueError('invalid device_group_name type:' +
                             'expected str, received {}'.format(
                                 type(device_group_name)))
        self.__device_group_name = device_group_name

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
        assert type(framework_id) is int
        self.__framework_id = framework_id

    @property
    def framework_name(self):
        """Returns the framework_name attribute.

        Args:
            framework_name (str): Value to set for the framework_name attribute
                of this object.
        """
        return self.__framework_name

    @framework_name.setter
    def framework_name(self, framework_name):
        assert type(framework_name) is str
        self.__framework_name = framework_name

    @property
    def device_id(self):
        """Returns the device_id attribute.

        Args:
            id (int): Value to set for the device_group_id attribute of this
                object.

        Raises:
            AssertionError: If supplied id value is not integer.
        """
        return self.__device_id

    @device_id.setter
    def device_id(self, id):
        assert type(id) is int
        self.__device_id = id

    # Additional Methods #

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

    def get_user_id(self):
        """Retrieves the user id for the currently authenticated user.

        This method is a wrapper around the Testdroid implementation.

        Returns:
            int: currently authenticated user id.

        Raises:
            RequestResponseError: If Testdroid responds with an error.
        """
        return self.client.get_me()['id']

    # Project operations #

    def get_projects(self):
        """Returns the list of projects.

        Returns:
            dict: Contains data on projects available on Bitbar.
        """
        existing_projects = self.client.get_projects()
        return existing_projects['data']

    def create_project(self, project_name, project_type,
                       permit_duplicate=False):
        """Creates a new Bitbar project using provided parameters.

        By default, Mozilla does not permit multiple projects with same name
        on Bitbar. This behavior can be overridden using the permit_duplicate
        parameter.

        If project creation is successful, relevant attributes of the new
        project is stored as object attributes.

        Args:
            project_name (str): Project name to be assigned to new project.
            project_type (str): Project type to be assigned to new project
            permit_duplicate (bool, optional): Permit creation of project even
                if existing project has same name.

        Raises:
            ProjectException: If permit_duplicate is False and project with
                same name is already on Bitbar.
        """
        if not permit_duplicate:
            try:
                existing_projects = self.get_projects()
                for project in existing_projects:
                    if project_name == project['name']:
                        raise ProjectException
            except ProjectException:
                msg = '{}: project_name: {} already exists'.format(
                    __name__,
                    project_name
                )
                raise ProjectException(msg)

        output = self.client.create_project(project_name, project_type)
        assert 'id' in output

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

    def get_project_configs(self):
        return self.client.get_project_config(self.project_id)

    def set_project_configs(self, new_config={}, path=None):
        """Overwrites part or all of project configuration with new values.

        Provided with either a dict of config values or path to a json file
        containing configs, this method will load the values, filter out
        values that are identical then modify the Bitbar project config
        with remaining values.

        Args:
            new_config (:obj:`dict`): Project configuration represented
                as dict.

        Raises:
            ProjectException: If new_config is not a valid dict.
            RequestResponseError: If new_config was not accepted by Bitbar
                due to type or value error.
        """
        if path:
            new_config = self._load_project_config(path)

        try:
            assert type(new_config) is dict
        except AssertionError:
            msg = '{}: config: not valid dict'.format(__name__)
            raise ProjectException(msg)

        existing_configs = self.get_project_configs()

        # filter new_configuration if existing_configs already contain the
        # same values, to avoid unnecessary operations to Bitbar.
        for key in list(new_config.keys()):
            if new_config.get(key) == existing_configs.get(key):
                new_config.pop(key)

        if len(new_config) is 0:
            msg = ''.join(['{}: no project configuration '.format(__name__),
                           'values to update on Bitbar'])
            print(msg)
            return

        self.client.set_project_config(self.project_id, new_config)

    def _load_project_config(self, path):
        new_config = json.loads(
            open(
                os.path.normpath(
                    os.path.join(
                        root_path(),
                        'project_config.json')), 'r').read())
        return new_config

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
                framework_name = str(framework[0])
                framework_id = int(framework[1])
                break

        if not framework_id:
            raise FrameworkException(
                'Invalid framework identifer provided: {}'.format(
                    kwargs.values()))

        self.client.set_project_framework(self.project_id, framework_id)
        self.framework_id = framework_id
        self.framework_name = framework_name

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
                  'skipping deletion..')
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
                msg = '{}: {} already exists on Bitbar, skipping'.format(
                    __name__,
                    filename
                )
                print(msg)
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

    def get_devices(self):
        """Returns the list of devices available on Bitbar.

        Returns:
            :obj:`list` of :obj:`dict`: List of currently available devices.

        Raises:
            RequestResponseError: If Testdroid responds with an error.
        """
        return self.client.get_devices()['data']

    def set_device_group(self, name=None, id=None):
        """Sets the project's device group to be used for test runs.

        Args:
            name (str, optional): Device group name in string.
            id (int, optional): Device group id in integer.

        Raises:
            DeviceException: If neither id nor name was supplied.
        """
        device_groups = [(device_group['id'], device_group['displayName'])
                         for device_group in self.get_device_groups()]

        for device_group in device_groups:
            # fill out missing parameter so we have both id and name.
            if name in device_group:
                id = device_group[0]
                break
            if id in device_group:
                name = device_group[1]
                break
            else:
                msg = '{}: use valid device group id or name'.format(
                    __name__
                )
                raise DeviceException(msg)

        self.device_group_id = id
        self.device_group_name = name

    def set_device(self, device_id):
        """Sets the device using the device_id.

        Accepts either a device name or device id.

        Args:
            device_id (int, str): Device specifier to be used to set the
                device_id attribute. Could be the device name (str) or
                device id (int).

        Raises:
            DeviceException: If device_id is not found in list of
                available device on Bitbar.
        """
        devices_list = self.get_devices()

        for device in devices_list:
            if device['id'] == device_id:
                self.device_id = device_id
                self.device_name = device['displayName']
                return
            if device['displayName'] == device_id:
                self.device_id = device['id']
                self.device_name = device_id
                return

        msg = '{}: device specifier {} not found on Bitbar.'.format(
            __name__,
            device_id
        )
        raise DeviceException(msg)

    # Test Run operations #

    def _is_test_name_unique(self, test_run_name):
        """Cross-checks provided test_run_name against all test run names.

        Args:
            test_run_name (str): Test run name to be compared against all
                previous test runs' names.

        Returns:
            bool: True if test name is unique. False otherwise.
            None: If test_run_name to be checked is None.
        """
        if test_run_name is not None:
            return test_run_name not in [run['displayName']
                                         for run in self.get_all_test_runs()]
        return None

    def start_test_run(self, **kwargs):
        """Starts a test run with parameters provided from the recipe.

        This method is a wrapper around the Testdroid implementation with
        additional operations. Parameters to this method should mirror that of
        the Testdroid implementation.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Raises:
            RequestResponseError: If Testdroid responds with an error.
        """
        try:
            assert self._is_test_name_unique(kwargs.get('name'))
        except AssertionError:
            raise TestException('{}: name: {} is not unique'.format(
                __name__,
                kwargs.get('name')
            ))

        self.test_run_id = self.client.start_test_run(self.project_id,
                                                      self.device_group_id,
                                                      **kwargs)
        self.test_run_name = self.get_test_run(self.test_run_id)

    def get_test_run(self, test_run_id=None, test_run_name=None):
        """Returns the test run details.

        Provided with integer value for test_run_id, if the test_run exists
        details for the test run is returned, including the current state
        and success status.

        Args:
            test_run_id (int): ID of the test run.

        Returns:
            :obj:`dict` of str: Dictionary of strings containing relevant
                test run information.

        Raises:
            RequestResponseError: If Testdroid responds with an error.
        """
        return self.client.get_test_run(self.project_id, test_run_id)

    def get_all_test_runs(self):
        """Returns all tests for the project.

        Returns:
            :obj:`dict` of str: Dictionary of strings holding all test run
                information for the project.
        """
        return self.client.get_project_test_runs(self.project_id)['data']

    def notify_test_run_complete(self, interval=30, timeout=300):
        """Waits for test run to complete and outputs status to the CLI.

        Args:
            interval (int, optional): Interval at which this method should
                query Bitbar for status updates for the test run.
            timeout (int, optional): Maximum time to wait before exiting the
                method.
        """
        total_wait_time = 0

        while (total_wait_time <= timeout):
            state = str(self.get_test_run(self.test_run_id)['state'])
            if state != 'FINISHED':
                time.sleep(interval)
                total_wait_time += interval
            else:
                break

        test_run_details = self.get_test_run(self.test_run_id)

        if total_wait_time >= timeout:
            print('Test run did not complete prior to {}s timeout.'.format(
                  timeout))
        print('Project Name:', self.project_name)
        print('Project Framework Name:', self.framework_name)
        print('Device Group Name:', self.device_group_name)
        print('Test Run Name:', self.test_run_name)
        print('Test Run State:', test_run_details['state'])
