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


from __future__ import absolute_import, division, print_function, unicode_literals

import os
import argparse
import collections
import logging
import sys

#from completer_extractor import completer_extractor as ce
from . import generate
from . import sdb_viewer

__author__ = "dave.mccoy@cospandesign.com (Dave McCoy)"

SCRIPT_NAME = os.path.basename(__file__)

DESCRIPTION = "SDB Tool"

COMPLETER_EXTRACTOR = False
TEMP_BASH_COMPLETER_FILEPATH = "sdb"

EPILOG = "Enter the toolname with a -h to find help about that specific tool\n"


TYPE_DICT = collections.OrderedDict()
TYPE_DICT["generate"] = "Generation of SDB ROM and associated cores"
TYPE_DICT["parser"] = "Parse SDB ROM data to a python structure of file"
TYPE_DICT["viewer"] = "View SDB structures"
TYPE_DICT["utility"] = "Functions to aid users in adapting SDB to their platform"


TOOL_DICT = collections.OrderedDict([
    (generate.NAME,{
        "type": "generate",
        "module": generate,
        "tool": generate.generate
    }),
    (sdb_viewer.NAME,{
        "type": "viewer",
        "module": sdb_viewer,
        "tool": sdb_viewer.view_sdb
    })
])



def update_epilog():
    global EPILOG
    tool_type_dict = collections.OrderedDict()
    for type_d in TYPE_DICT:
        tool_type_dict[type_d] = {}
        tool_type_dict[type_d]["description"] = TYPE_DICT[type_d]
        tool_type_dict[type_d]["tools"] = []

    for tool in TOOL_DICT:

        tool_type_dict[TOOL_DICT[tool]["type"]]["tools"].append(tool)

    EPILOG += "\n"
    EPILOG += "Tools:\n\n"
    for tool_type in tool_type_dict:
        #EPILOG += "{0}\n\n".format(tool_type_dict[tool_type]["description"])
        for tool in tool_type_dict[tool_type]["tools"]:
            EPILOG += "{0:5}{1:20}{2}\n".format("", tool, TOOL_DICT[tool]["module"].DESCRIPTION)
        EPILOG += "\n"

    EPILOG += "\n"

def main():
    update_epilog()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION,
        epilog=EPILOG
    )

    #Setup the status message
    #s = status.Status()
    #s.set_level(status.StatusLevel.INFO)

    #Global Flags
    parser.add_argument("-d", "--debug", action='store_true', help="Output test debug information")


    subparsers = parser.add_subparsers( title = "Tools",
                                        description = DESCRIPTION,
                                        metavar = None,
                                        dest = "tool")


    for tool in TOOL_DICT:
        p = subparsers.add_parser(tool,
                                  description=TOOL_DICT[tool]["module"].DESCRIPTION,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
        TOOL_DICT[tool]["module"].setup_parser(p)
        TOOL_DICT[tool]["parser"] = p


    #Parse the arguments
    if COMPLETER_EXTRACTOR:
        ce(parser, TEMP_BASH_COMPLETER_FILEPATH)
        return

    args = parser.parse_args()


    #Configure the Logger
    log = logging.getLogger('sdb')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(filename)s:%(module)s:%(funcName)s: %(message)s')

    #Create a Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)

    if args.debug:
        log.setLevel(logging.DEBUG)

    TOOL_DICT[args.tool]["tool"](args)


