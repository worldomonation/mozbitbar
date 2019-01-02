# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import logging

default_fmt = ' - '.join([
    '%(asctime)s',
    '%(levelname)s',
    '%(module)s:%(funcName)s',
    '%(message)s'
])


def setup_logger(config=None):
    """Sets up the logging facilities.

    Args:
        config (:obj:`dict`, optional): Optional dictionary specifying custom
            values to set.

    Returns:
        :obj:`logging`: Instance of logging object instantiated with
            pre-set values.
    """
    fmt = (getattr(config, 'fmt', None) or default_fmt)
    formatter = logging.Formatter(fmt=fmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(getattr(config, 'name', None) or 'mozbitbar')
    # very important to stop duplicate logging entries
    logger.propagate = False
    logger.setLevel(
        logging.DEBUG if getattr(config, 'verbose', None) else logging.INFO)

    if not logger.handlers:
        logger.addHandler(handler)
    return logger
