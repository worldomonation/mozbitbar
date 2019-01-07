# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import pytest


@pytest.mark.parametrize('kwargs,expected', [
    (
        1,
        1
    )
])
def test_set_device_group(kwargs, expected):
    pass
