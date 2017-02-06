# The MIT License (MIT)
# Copyright (c) 2016 by the Cate Development Team and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Description
===========

Provides random utility functions.

*Implementation note: this module shall not have any dependencies to higher-level Cate modules.*

Verification
============

The module's unit-tests are located in
`test/test_misc.py <https://github.com/CCI-Tools/cate-core/blob/master/test/test_misc.py>`_ and may be executed using
``$ py.test test/test_misc.py --cov=cate/core/misc.py`` for extra code coverage information.

Components
==========
"""

__author__ = "Norman Fomferra (Brockmann Consult GmbH)"

from .extend import extend
from .misc import *
from .monitor import Monitor, ChildMonitor, ConsoleMonitor
from .namespace import Namespace
from .undefined import UNDEFINED