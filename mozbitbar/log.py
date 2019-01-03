# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import logging

_default_fmt = ' - '.join([
    '%(asctime)s',
    '%(levelname)s',
    '%(module)s:%(funcName)s',
    '%(message)s'
])


def setup_logger(**config):
    """Sets up the logging facilities.

    Args:
        config (:obj:`dict`, optional): Optional dictionary specifying custom
            values to be used for the initialization of logging facility.

    Returns:
        :obj:`logging`: Instance of logging object.
    """
    fmt = (config.get('fmt') or _default_fmt)
    formatter = logging.Formatter(fmt=fmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(config.get('name') or 'mozbitbar')
    # very important to stop duplicate logging entries
    logger.propagate = False
    if config.get('verbose'):
        logger.setLevel(logging.DEBUG)
    elif config.get('quiet'):
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)

    if logger.handlers:
        for old_handler in logger.handlers:
            logger.removeHandler(old_handler)

    if not logger.handlers:
        logger.addHandler(handler)
    return logger
