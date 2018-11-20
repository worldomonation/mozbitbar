from __future__ import print_function, absolute_import

from mozbitbar.configuration import Configuration
from testdroid import Testdroid
from testdroid import RequestResponseError

class Bitbar(Configuration):
    def __init__(self):
        super(Bitbar, self).__init__()