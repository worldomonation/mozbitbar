# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import logging
import sys

import yaml

from testdroid import RequestResponseError

try:
    from mozbitbar.bitbar_project import BitbarProject
except ImportError:
    from bitbar_project import BitbarProject

try:
    from mozbitbar.recipe import Recipe
except ImportError:
    from recipe import Recipe

try:
    from mozbitbar import (
        MozbitbarRecipeException,
        MozbitbarProjectException,
        MozbitbarCredentialException,
        MozbitbarFrameworkException,
        MozbitbarFileException,
        MozbitbarTestRunException,
        MozbitbarDeviceException,
    )
except ImportError:
    from __init__ import (
        MozbitbarRecipeException,
        MozbitbarProjectException,
        MozbitbarCredentialException,
        MozbitbarFrameworkException,
        MozbitbarFileException,
        MozbitbarTestRunException,
        MozbitbarDeviceException,
    )


logger = logging.getLogger('mozbitbar')


def initialize_recipe(recipe_name):
    """Initializes the Recipe object.

    Given a path to the recipe file, this method will initialize and return
    an instance of the Recipe object, containing within it required project
    parameters for interacton with Bitbar. Also contained within this object
    is the internal representation of the tasks to be executed.

    Args:
        recipe_name (str): Path to the recipe.

    Returns:
        :obj:`Recipe`: An instance of a recipe to be executed.

    Raises:
        SystemExit: If path to the recipe is invalid, or the recipe is
            not compliant.
    """
    logger.info('Recipe object initialization...')
    try:
        logger.info('Recipe object successfully initialized.')
        return Recipe(recipe_name)
    except MozbitbarRecipeException as re:
        logger.critical(re.message)
        sys.exit(1)


def initialize_bitbar(recipe, credentials=None):
    """Initializes the Bitbar Project object.

    Given a valid recipe, this method will instantiate and return an instance
    of the BitbarProject object, used to interact with Bitbar and execute
    actions.

    Args:
        recipe (:obj:`Recipe`): An instance of a Recipe object.

    Raises:
        SystemExit: If provided Recipe object contains invalid project
            parameters, or Testdroid credentials were missing or invalid.
    """
    if credentials:
        logger.info('Credential file specified.')
        with open(credentials, 'r') as f:
            loaded_credentials = yaml.load(f.read())
        for c in loaded_credentials:
            recipe.project_arguments.update(c)

    logger.info('Bitbar project initialization...')
    try:
        logger.info('Bitbar project object successfully initialized.')
        return BitbarProject(recipe.project,
                             **recipe.project_arguments)
    except (MozbitbarProjectException, MozbitbarCredentialException) as e:
        logger.critical(e.message)
        sys.exit(1)


def run_recipe(recipe_name, args):
    """Executes all actions defined in a recipe.

    This method will first initialize an instance of a Recipe object to
    hold recipe-related data.

    Subsequently an instance of a BitbarProject object is initialized which
    will hold data related to a Bitbar project.

    If both objects pass validation, the recipe is executed in sequential
    order.

    Args:
        recipe_name (str): Either a fully qualified path, or base name of the
            recipe to be run.

    Raises:
        SystemExit: If recipe specified an action that is not implemented,
            or any other errors were encountered while actions were being
            executed.
    """
    # example implementation showing how the process may look like.
    # using the recipe, this method will parse actions that need to be done,
    # and automatically call the action from an instance of BitbarProject
    # object. As long as the recipe is defined with the action that matches
    # the method name, and the appropriate arguments are provided,
    # this method will execute each action automatically.
    recipe = initialize_recipe(recipe_name)

    bitbar_project = initialize_bitbar(recipe, args.credentials)

    logger.info('Start executing Bitbar tasks defined in recipe...')
    for task in recipe.task_list:
        action = task.pop('action')
        arguments = task.pop('arguments', {})
        logger.debug(' '.join(['Action to run:', action]))

        func = getattr(bitbar_project, action, None)
        if func:
            try:
                func(**arguments)
            except RequestResponseError as rre:
                logger.info('Testdroid raised an exception:')
                print('Status code: ', rre.status_code)
                print(rre.message)
                sys.exit(1)
            except (MozbitbarCredentialException,
                    MozbitbarProjectException,
                    MozbitbarFrameworkException,
                    MozbitbarFileException,
                    MozbitbarDeviceException,
                    MozbitbarTestRunException):
                # If there's a better way to catch multiple exceptions derived
                # from the same base class - I'd like to know.
                msg = ' '.join([
                    'Encountered exception when executing task: ',
                    '{}'.format(action)
                ])
                logger.exception(msg)
                sys.exit(1)
        else:
            msg = ' '.join([
                'Specified action not implemented:',
                '{}'.format(action)
            ])
            logger.critical(msg)
            sys.exit(1)
