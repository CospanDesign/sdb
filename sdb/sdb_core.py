# this file is part of SDB.
#
# SDB is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SDB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SDB.  If not, see <http://www.gnu.org/licenses/>


from __future__ import absolute_import, division, print_function, unicode_literals

__author__ = "dave.mccoy@cospandesign.com (Dave McCoy)"

from array import array as Array
import collections


class SDBError(Exception):
    pass

class SDBWarning(Exception):
    pass

class SDBInfo(Exception):
    pass

class SDB (object):

    def __init__(self):
        self.d = {}

        for e in self.ELEMENTS:
            self.d[e] = ""

