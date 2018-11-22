from __future__ import print_function, absolute_import

import os
import yaml

from mozbitbar.bitbar_project import BitbarProject
from mozbitbar import InvalidRecipeException


class Recipe(object):
    def __init__(self, recipe_name):
        """Initializes an instance of a Recipe object.

        Upon initialization, a valid recipe name that corresponds
        to a stored recipe is expected.
        """
        # store provided name
        self.recipe_name = recipe_name
        # parse recipe and perform sanitizing operations
        self.load_recipe_from_yaml()
        self.split_project_parameters()

    def load_recipe_from_yaml(self):
        """Parses a recipe from a YAML file stored locally.
        """
        # need to handle cases where recipe is not in relative path
        path = os.path.normpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'recipes', self.recipe_name))

        with open(path, 'r') as f:
            self.task_list = yaml.load(f)

    def split_project_parameters(self):
        """Separates project identifier from stored recipe from rest of recipe.

        This step is necessary as all recipes should define either:
            - existing project to be run against
            - new project
        """
        for index, task in enumerate(self.task_list):
            # project parameters defined in recipe
            if task.get('project'):
                self.project = task.get('project')
            self.project_arguments = task.get('arguments')
            self.task_list.pop(index)
            return

        # project parameters not found in recipe
        raise InvalidRecipeException('Project parameters not found in recipe: {}.'.format(self.recipe_name))

    def get_task_list(self):
        """Returns the list of tasks that make up the recipe.
        """
        return self.task_list


def run_recipe(recipe_name):
    """Example implementation showing how the process may look like.

    This method should handle any methods that are implemented in the
    Bitbar related classes, provided the recipe properly specifies the
    name of action and any required parameters exactly.
    """
    recipe = Recipe(recipe_name)
    bitbar_project = BitbarProject(recipe.project, **recipe.project_arguments)

    for task in recipe.get_task_list():
        action = task.pop('action')
        arguments = task.pop('arguments')

        func = getattr(bitbar_project, action, None)
        if func:
            func(**arguments)
