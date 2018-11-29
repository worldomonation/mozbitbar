from __future__ import print_function, absolute_import

import os
import sys
import yaml

from mozbitbar.bitbar_project import BitbarProject
from mozbitbar import (
    InvalidRecipeException,
    ProjectException,
    FrameworkException,
    CredentialException,
    OperationNotImplementedException,
    DeviceException,
    TestException
    )
from testdroid import RequestResponseError
from yaml.scanner import ScannerError


class Recipe(object):
    def __init__(self, recipe_name):
        """Initializes an instance of a Recipe object.

        Upon initialization, a valid recipe name that corresponds
        to a stored recipe is expected.

        Args:
            recipe_name (str): Base name or fully qualified path to the recipe
                to be loaded.
        """
        self.locate_recipe(recipe_name)

        self.load_recipe_from_yaml()

    @property
    def recipe_name(self):
        """Returns the base name of the recipe.

        Args:
            recipe_name (str): Base name of the recipe.
        """
        return self.__recipe_name

    @recipe_name.setter
    def recipe_name(self, recipe_name):
        self.__recipe_name = os.path.basename(recipe_name)

    @property
    def recipe_path(self):
        """Returns the absolute path to the recipe.

        Args:
            path (str): Absolute path to the recipe.
        """
        return self.__recipe_path

    @recipe_path.setter
    def recipe_path(self, path):
        self.__recipe_path = os.path.abspath(path)

    @property
    def task_list(self):
        """Returns the task list for the loaded recipe.

        Validation is performed when setting this value.

        Args:
            task_list (:obj:`list` of :obj:`dict`): List of tasks defined by
                recipe.
        """
        return self.__task_list

    @task_list.setter
    def task_list(self, task_list):
        assert type(task_list) is list
        for action in task_list:
            assert type(action) is dict
            assert 'action' in action
            assert 'arguments' in action
        self.__task_list = task_list

    @property
    def project_arguments(self):
        """Returns the project_argument attribute.

        Args:
            project_arguments (:obj:`dict` of str): Arguments related to
                the selection or creation of a project.
        """
        return self.__project_arguments

    @project_arguments.setter
    def project_arguments(self, project_arguments):
        assert type(project_arguments) is dict

        self.__project_arguments = project_arguments

    def locate_recipe(self, path):
        """Locates a recipe on the local disk.

        Args:
            path (str): Base filename or fully qualified path on local disk.

        Raises:
            IOError: If path is neither a file in current working directory nor
                a fully qualified path on local disk.
        """
        if os.path.isfile(path):
            self.recipe_name = path
            self.recipe_path = path
        else:
            msg = '{name}: recipe not found at: {path}'.format(
                name=__name__,
                path=path
            )
            raise IOError(msg)

    def load_recipe_from_yaml(self):
        """Parses a recipe from a YAML file stored locally.

        The loaded YAML-formatted recipe is put through validation prior to
        being saved into this object.

        Raises:
            IOError: If recipe path does not map to a file on local disk.
            InvalidRecipeException: If file specified by recipe path is not a
                valid YAML file.
        """
        try:
            with open(self.recipe_path, 'r') as f:
                self.validate_recipe(yaml.load(f))
        except ScannerError:
            msg = '{}: {} is not a valid YAML file.'.format(
                __name__,
                self.recipe_path
            )
            raise InvalidRecipeException(msg)

    def validate_recipe(self, recipe):
        """Validates the loaded recipe.

        In the first step, the presence of a project specifier in the recipe
        is checked. This step is necessary as recipes need to specify one of:
            - existing project to be run against
            - creation of a new project

        Once the project specifier is validated, rest of the recipe is saved
        to the task_list attribute.

        Raises:
            InvalidRecipeException: If recipe does not contain a valid project
                specifier.
        """
        for index, task in enumerate(recipe):
            if task.get('project'):
                # project specifier found in recipe. Remove it from the recipe
                # and store it in its own attributes.
                self.project = task.get('project')
                self.project_arguments = task.get('arguments')
                recipe.pop(index)

        try:
            assert self.project
            assert self.project_arguments
        except AssertionError:
            msg = '{}: project specifier not found in recipe: {}'.format(
                __name__,
                self.recipe_name
            )
            raise InvalidRecipeException(msg)

        # remaining recipe object is the list of actions to run.
        self.task_list = recipe


def run_recipe(recipe_name):
    """Runs an instance of a recipe.

    Initializes an instance of a Recipe object to hold recipe-related data.

    Subsequently an instance of a BitbarProject object is initialized which
    will hold data related to a Bitbar project.

    If both objects pass validation, the recipe is executed sequentially from
    beginning.

    Args:
        recipe_name (str): Either a fully qualified path, or base name of the
            recipe to be run.

    Raises:
        OperationNotImplementedException: If recipe specified an action that
            is not implemented in BitbarProject.
    """
    # example implementation showing how the process may look like.
    # using the recipe, this method will parse actions that need to be done,
    # and automatically call the action from an instance of BitbarProject
    # object. As long as the recipe is defined with the action that matches
    # the method name, and the appropriate arguments are provided,
    # this method will execute each action automatically.
    try:
        recipe = Recipe(recipe_name)
    except IOError as ie:
        print(ie.message)
        sys.exit(1)
    try:
        bitbar_project = BitbarProject(recipe.project,
                                       **recipe.project_arguments)
    except ProjectException as pe:
        print(pe.message)
        sys.exit(1)

    for task in recipe.task_list:
        action = task.pop('action')
        arguments = task.pop('arguments')

        func = getattr(bitbar_project, action, None)
        if func:
            try:
                func(**arguments)
            except RequestResponseError as rre:
                print('Testdroid raised an exception:')
                print('Status code: ', rre.status_code)
                print(rre.message)
            except InvalidRecipeException as ire:
                print(ire.message)
            except ProjectException as pe:
                print(pe.message)
            except FrameworkException as fe:
                print(fe.message)
            except CredentialException as ce:
                print(ce.message)
            except DeviceException as de:
                print(de.message)
            except TestException as te:
                print(te.message)
        else:
            msg = '{}: action: {} not found in BitbarProject.'.format(
                __name__,
                action
            )
            raise OperationNotImplementedException(msg)
