from __future__ import print_function, absolute_import

import os
import yaml

from testdroid import Testdroid


client = Testdroid(username=os.environ.get('TESTDROID_USERNAME'),
                   password=os.environ.get('TESTDROID_PASSWORD'),
                   apikey=os.environ.get('TESTDROID_APIKEY'),
                   url=os.environ.get('TESTDROID_URL'))


def parse_stored_recipe(recipe_name):
    path = os.path.normpath(os.path.join(
        '/Users/egao/workspace/mozbitbar/mozbitbar/recipes', recipe_name))

    with open(path, 'r') as f:
        recipe = yaml.load(f)

    return recipe


def run_single_recipe(recipe):
    action = recipe.pop('action')
    func = getattr(client, action)
    if func:
        return func(**recipe['arguments'])


def run_recipes(recipe_name):
    recipes = parse_stored_recipe(recipe_name)

    for index in range(len(recipes)):
        recipe = recipes.pop(index)
        run_single_recipe(recipe)