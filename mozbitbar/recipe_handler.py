from __future__ import print_function, absolute_import

import os
import yaml

from mozbitbar.bitbar_project import BitbarProject
from mozbitbar import (
    InvalidRecipeException,
    ProjectException,
    FrameworkException,
    CredentialException,
    OperationNotImplementedException
    )
from testdroid import RequestResponseError


class Recipe(object):
    def __init__(self, recipe_name):
        """Initializes an instance of a Recipe object.

        Upon initialization, a valid recipe name that corresponds
        to a stored recipe is expected.

        Args:
            recipe_name (str): Name of the recipe file to be parsed.
        """
        # store provided name
        self.recipe_name = recipe_name
        # parse recipe and perform sanitizing operations
        self.load_recipe_from_yaml()
        self.split_project_parameters()

    def load_recipe_from_yaml(self):
        """Parses a recipe from a YAML file stored locally.
        """
        # TODO: need to handle cases where recipe is not found.
        path = os.path.normpath(
            os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)), 'recipes', self.recipe_name))

        with open(path, 'r') as f:
            self.task_list = yaml.load(f)

    def split_project_parameters(self):
        """Separates project identifier from stored recipe from rest of recipe.

        This step is necessary as recipes need to specify one of:
            - existing project to be run against
            - creation of a new project

        Raises:
            InvalidRecipeException: If recipe does not contain a valid project
                specifier.
        """
        for index, task in enumerate(self.task_list):
            # project parameters defined in recipe
            if task.get('project'):
                self.project = task.get('project')
            self.project_arguments = task.get('arguments')
            self.task_list.pop(index)
            return

        # project parameters not found in recipe
        msg = '{name}: project specifier not found in recipe: {recipe}'.format(
            name=__name__,
            recipe=self.recipe_name)
        raise InvalidRecipeException(msg)

    def get_task_list(self):
        """Returns the list of tasks that make up the recipe.
        """
        return self.task_list


def run_recipe(recipe_name):
    """Runs an instance of a recipe.

    Initializes an instance of a Recipe object to hold recipe-related data.

    Subsequently an instance of a BitbarProject object is initialized which
    will hold data related to a Bitbar project.

    If both objects pass validation, the recipe is executed sequentially from
    beginning.
    """
    # example implementation showing how the process may look like.
    # using the recipe, this method will parse actions that need to be done,
    # and automatically call the action from an instance of BitbarProject
    # object. As long as the recipe is defined with the action that matches
    # the method name, and the appropriate arguments are provided,
    # this method will execute each action automatically.
    recipe = Recipe(recipe_name)
    bitbar_project = BitbarProject(recipe.project, **recipe.project_arguments)

    for task in recipe.get_task_list():
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
        else:
            msg = '{name}: action {action} not found in BitbarProject.'.format(
                name=__name__,
                action=action)
            raise OperationNotImplementedException(msg)
