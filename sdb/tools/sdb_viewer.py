# Distributed under the MIT licesnse.
# Copyright (c) 2014 Dave McCoy (dave.mccoy@cospandesign.com)

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




