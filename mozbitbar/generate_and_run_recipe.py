# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import os
import subprocess
import sys

import yaml

mozbitbar_repository = 'https://github.com/worldomonation/mozbitbar.git'
mozilla_docker_repository = 'https://github.com/bclary/mozilla-bitbar-docker.git'
clone_base_dir = os.path.abspath(os.getcwd())
# docker_version = None
docker_version = 'test_string'


def clone_repository():
    mozbitbar_clone_status = subprocess.call(
        ' '.join([
            'git clone',
            mozbitbar_repository,
            clone_base_dir
        ])
    )
    mozilla_docker_status = subprocess.call(
        ' '.join([
            'git clone',
            mozilla_docker_repository,
            clone_base_dir
        ])
    )

    # exit codes are non-zero for failures so any() will eval to True
    if any([mozbitbar_clone_status, mozilla_docker_status]):
        print('Failed to clone dependent repository.')
        sys.exit(1)

    if (os.path.exists(os.path.join(clone_base_dir, 'mozbitbar')) and
        os.path.exists(os.path.join(clone_base_dir, 'mozilla-bitbar-docker.git'))):
        return clone_base_dir

    return None


def build_docker_image():
    build_status = subprocess.call(
        ' '.join(['bash', 'mozilla-bitbar-docker/build.sh'])
    )

    if build_status:
        print('Could not build required package.')

    version_path = os.path.join(
        clone_base_dir, 'mozilla-bitbar-docker', 'version')
    with open(version_path, 'r') as f:
        docker_version = f.read().rstrip()
        return True

    return False

def update_recipe(args):
    # this is working under assumption that recipe is already defined, so the
    # only action that needs to occur is to update the DOCKER_IMAGE_VERSION
    # parameter. This may or may not be a valid assumption.
    if args.recipe:
        with open(args.recipe, 'r') as f:
            recipe = yaml.load(f.read())

    if docker_version:
        for index, action in enumerate(recipe):
            if action['action'] == 'set_project_parameters':
                # if set_project_parameters exists, the appropriate parameter
                # value must be refreshed, and Bitbar told to overwrite
                # existing parameter with new values
                parameter_list = action['arguments']['parameters']
                index = [
                    index for index, parameter in enumerate(parameter_list)
                        if parameter['key'] == 'DOCKER_IMAGE_VERSION'
                ]

                if index:
                    parameter_list[index]['value'] == docker_version
                else:
                    parameter_list.append(dict(key='DOCKER_IMAGE_VERSION',value=docker_version))

                action['arguments']['force_overwrite'] = True

            elif 'test_run' in action.get['action']:
                set_docker_image_version_action = {
                    'action': 'set_project_parameters',
                    'arguments': {
                        'force_overwrite': True,
                        'parameters': [
                            {
                                'key': 'DOCKER_IMAGE_VERSION',
                                'value': docker_version
                            }
                        ]
                    }
                }
                # if set_project_parameter does not exist, perform such action
                # immediately prior to any test runs being started
                recipe.insert(index, set_docker_image_version_action)
    else:
        return None


def run(args):
    # clone_repository()
    # build_docker_image()
    update_recipe(args)
