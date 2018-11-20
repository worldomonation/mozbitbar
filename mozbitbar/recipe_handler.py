from __future__ import print_function, absolute_import

import os
import yaml

from mozbitbar.bitbar_project import BitbarProject


class Recipe(object):
    def __init__(self, recipe_name):
        # store provided name
        self.recipe_name = recipe_name
        # parse recipe and perform sanitizing operations
        self.load_recipe_from_yaml()
        self.split_project_id_from_recipe()

    def load_recipe_from_yaml(self):
        # need to handle cases where recipe is not in relative path
        path = os.path.normpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'recipes', self.recipe_name))

        with open(path, 'r') as f:
            self.task_list = yaml.load(f)

    def split_project_id_from_recipe(self):
        for index, task in enumerate(self.task_list):
            if task.get('project_id'):
                self.project_id = task.get('project_id')
                self.new_project_arguments = task.get('arguments')
                self.task_list.pop(index)

    def get_task_list(self):
        return self.task_list


def run_recipe(recipe_name):
    recipe = Recipe(recipe_name)
    if recipe.new_project_arguments:
        bitbar_project = BitbarProject(**recipe.new_project_arguments)
    else:
        bitbar_project = BitbarProject(recipe.project_id)

    for task in recipe.get_task_list():
        testdroid_action = task.pop('action')
        testdroid_arguments = task.pop('arguments')

        func = getattr(bitbar_project, testdroid_action, None)
        if func:
            func(**testdroid_arguments)
