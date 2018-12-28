# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import logging

fmt = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'


def setup_logger():
    formatter = logging.Formatter(fmt=fmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger('mozbitbar')
    # very important to stop duplicate logging entries
    logger.propagate = False
    # TODO: support debug level after reading contents of cli arguments
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        logger.addHandler(handler)
    return logger
