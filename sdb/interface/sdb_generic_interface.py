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


import sys
import os


from __future__ import absolute_import, division, print_function, unicode_literals

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from . import sdb_object_model

#Helper functions to create all aspects of an an SDB ROM
from .sdb_component import create_device_record
from .sdb_component import create_interconnect_record
from .sdb_component import create_bridge_record
from .sdb_component import create_integration_record
from .sdb_component import create_synthesis_record
from .sdb_component import create_repo_url_record

from .sdb_component import convert_rom_to_32bit_buffer


class SDBGeneratorError(Exception):
    pass

class SDBParserError(Exception):
    pass

class SDBGenericInterface(object):
    def __init__(self):
        self.som = sdb_object_model.SOM()
        pass


    def _generate_sdb_rom(self, sdb_config):
        """
        Parse a python dictionary to an SDB configuration
        """
        pass

    def generate_sdb_rom(self, user_data):
        """
        User defined function, this should be overriden from the user defined
        parser/generated user should call the internal _generate_sdb_rom
        function with a dictionary of your parsed data

        Args:
            user_data (??): All data to parse our your version of the ROM

        Returns:
            Nothing

        Raises:
            SDBGeneratorError
        """
        raise AssertionError("Subclass must override this function")

    def _parse_sdb_rom(self, rom):
        """
        Parse an SDB ROM to a python based dictionary
        """ 
        pass



    def parse_sdb_rom(self, user_data):
        """
        User defined function, this should be overriden from the user defined
        parser/generated user should call the internal _parse_sdb_rom, it will
        return a SDB Object Mode that can be used to instantiate user Drivers.

        As an example the user_data can simply be the ROM obtained from the
        FPGA or it can be a tuple containing the ROM as well as any use specific
        data

        Args:
            user_data (??): Implementation specific user data that the function
                uses to perform all the specific parser info


        Returns (SOM): SDB Object Model that can be used to figure out what is
            in the FPGA
        """
        raise AssertionError("Subclass must override this function")


