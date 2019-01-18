# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import logging
import sys
import traceback

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
        MozbitbarOperationNotImplementedException,
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
        MozbitbarOperationNotImplementedException,
    )

logger = logging.getLogger('mozbitbar')


def initialize_recipe(recipe_name):
    logger.info('Recipe object initialization...')
    try:
        logger.info('Recipe object successfully initialized.')
        return Recipe(recipe_name)
    except MozbitbarRecipeException as re:
        logger.critical(re.message)
        sys.exit(1)


def initialize_bitbar(recipe):
    logger.info('Bitbar project initialization...')
    try:
        logger.info('Bitbar project object successfully initialized.')
        return BitbarProject(recipe.project,
                             **recipe.project_arguments)
    except (MozbitbarProjectException, MozbitbarCredentialException) as e:
        logger.critical(e.message)
        sys.exit(1)


def run_recipe(recipe_name):
    """Executes actions in a recipe.

    Initializes an instance of a Recipe object to hold recipe-related data.

    Subsequently an instance of a BitbarProject object is initialized which
    will hold data related to a Bitbar project.

    If both objects pass validation, the recipe is executed sequentially from
    beginning.

    Args:
        recipe_name (str): Either a fully qualified path, or base name of the
            recipe to be run.

    Raises:
        MozbitbarOperationNotImplementedException: If recipe specified an
            action that is not implemented in BitbarProject.
    """
    # example implementation showing how the process may look like.
    # using the recipe, this method will parse actions that need to be done,
    # and automatically call the action from an instance of BitbarProject
    # object. As long as the recipe is defined with the action that matches
    # the method name, and the appropriate arguments are provided,
    # this method will execute each action automatically.
    recipe = initialize_recipe(recipe_name)

    bitbar_project = initialize_bitbar(recipe)

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
                logger.critical('Encountered an exception while executing task: \
                                {}'.format(action))
                tb = traceback.extract_stack()
                logger.critical('Exception details: {}'.format(
                                "".join(traceback.format_list(tb)[:-1])))
                sys.exit(1)
        else:
            msg = 'Specified action not implemented in BitbarProject: \
                   {}'.format(action)
            logger.critical(msg)
            sys.exit(1)
