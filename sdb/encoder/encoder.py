#! /usr/bin/env python

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


class Encoder(object):
    """
    Encoder class, base class for all encoders. encoder implementations
    should subclass this. The output of the encoder is a generic SDB
    object model.
    """
    def __init__(self):
        pass

    def encode(self, raw_data):
        """
        This is where the actual encoding happens, the output of this
        is a SOM with the protocol specific data is converted to a
        generic SOM that can be used in all applications

        Args:
            raw_data: Data in any format the protocol requires, there
            is no limitation on this protocol

        Returns:
            SOM
        """
        pass
