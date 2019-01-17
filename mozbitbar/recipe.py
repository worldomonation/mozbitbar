# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import logging
import os

import yaml
from yaml.reader import ReaderError
from yaml.scanner import ScannerError

try:
    from mozbitbar import MozbitbarRecipeException
except ImportError:
    from __init__ import MozbitbarRecipeException


logger = logging.getLogger('mozbitbar')


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
        content = self.load_recipe_from_yaml()
        self.validate_recipe(content)

    @property
    def recipe_name(self):
        """Returns the base name of the recipe.

        Args:
            recipe_name (str): Base name of the recipe.
        """
        return self.__recipe_name

    @recipe_name.setter
    def recipe_name(self, recipe_name):
        self.__recipe_name = recipe_name

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
        if type(task_list) is not list:
            raise TypeError('Recipe task list must be of type list.')
        for action in task_list:
            if type(action) is not dict:
                raise TypeError('Recipe action must be of type dict.')
            if 'action' not in action:
                msg = 'Recipe action must contain key value: action.'
                raise MozbitbarRecipeException(message=msg)
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
        if not type(project_arguments) is dict:
            msg = 'Project arguments must be of type dict, got {}.'.format(
                type(project_arguments))
            raise TypeError(msg)
        if not bool(project_arguments):
            msg = 'Project arguments must not be empty.'
            raise MozbitbarRecipeException(message=msg)

        self.__project_arguments = project_arguments

    def locate_recipe(self, path):
        """Locates a recipe on the local disk.

        Args:
            path (str): Base filename or fully qualified path on local disk.

        Raises:
            MozbitbarRecipeException: If path is neither a file in current
                working directory nor a fully qualified path on local disk.
        """
        logger.debug('Recipe path: {}'.format(path))
        if os.path.isfile(path):
            self.recipe_name = os.path.basename(path)
            self.recipe_path = path
        else:
            msg = '{name}: recipe not found at: {path}'.format(
                name=__name__,
                path=path
            )
            raise MozbitbarRecipeException(message=msg)

    def load_recipe_from_yaml(self):
        """Parses a recipe from a YAML file stored locally.

        The loaded YAML-formatted recipe is put through validation prior to
        being saved into this object.

        Raises:
            IOError: If recipe path does not map to a file on local disk.
            MozbitbarRecipeException: If file specified by recipe path
                is not a valid YAML file.
        """
        try:
            with open(self.recipe_path, 'r') as f:
                return yaml.load(f.read())
        except (ScannerError, ReaderError):
            msg = 'Invalid YAML file: {}'.format(self.recipe_path)
            raise MozbitbarRecipeException(message=msg)

    def validate_recipe(self, recipe):
        """Validates the loaded recipe.

        In the first step, the presence of a project specifier in the recipe
        is checked. This step is necessary as recipes need to specify one of:
            - existing project to be run against
            - creation of a new project

        Once the project specifier is validated, rest of the recipe is saved
        to the task_list attribute.

        Raises:
            MozbitbarRecipeException: If recipe does not contain a
                valid project specifier.
        """
        for index, task in enumerate(recipe):
            if task.get('project'):
                # project attribute must be specified, otherwise
                # no further operations can take place
                self.project = task.get('project')
                self.project_arguments = task.get('arguments')
                # remove the project related item from the list
                recipe.pop(index)
                break
            else:
                msg = 'Project specifier missing from recipe.'
                raise MozbitbarRecipeException(message=msg)

        self.task_list = recipe
