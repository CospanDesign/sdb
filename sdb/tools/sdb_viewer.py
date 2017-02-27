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

import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from som_rom_parser import parse_rom_image

NAME = "sdb-viewer"
SCRIPT_NAME = "sdb %s" % NAME

__author__ = "dave.mccoy@cospandesign.com (Dave McCoy)"

DESCRIPTION = "display the contents of the SDB of the specified file"

EPILOG = "\n"


def setup_parser(parser):
    parser.description = DESCRIPTION
    parser.add_argument("filename",
                        type=str,
                        nargs=1,
                        help="Specify a file to read containing an SDB image")
    return parser


def view_sdb(args):
    parse_sdb_file(args.filename[0])
    sys.exit(0)

def parse_sdb_file(filename):
    if not os.path.exists(filename):
        raise IOError("File: %s does not exist!", filename)
    f = open(filename, 'r')
    buf = f.read()
    f.close()
    som = parse_rom_image(buf)
    som.pretty_print_sdb()




