# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, absolute_import

import pytest


@pytest.mark.parametrize('args,expected', [
    (
        []
    )
])
def test_parse_arguments(args, expected):
