#! /usr/bin/python

#Distributed under the MIT licesnse.
#Copyright (c) 2013 Dave McCoy (dave.mccoy@cospandesign.com)

#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#of the Software, and to permit persons to whom the Software is furnished to do
#so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import json
import logging
from collections import OrderedDict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import sdb_object_model
import sdb_component

NAME = "generate"
SCRIPT_NAME = "sdb %s" % NAME

__author__ = "dave.mccoy@cospandesign.com (Dave McCoy)"

DESCRIPTION = "Generate an SDB from a JSON configuration file"

EPILOG = "Currently the only input format is json\n"       \
         "Currently the only output format is a 32-bit hex ROM that can installed into a block RAM\n" \
         "Examples\n"\
         "Read in an SDB in a JSON format and generate a 32-bit ROM file\n" \
         "\tsdb %s --format rom /path/to/json_config.json\n" % NAME

def setup_parser(parser):
    parser.description = DESCRIPTION
    parser.add_argument("--iformat", type=str, nargs='*', default=["json"], help="Specify the configuration format (default: json)")
    parser.add_argument("--oformat", type=str, nargs='*', default=["rom"], help="Specify the type of output to generate (default: rom)")
    parser.add_argument("filename", type=str, nargs=1, help="Specify a file used to generate an SDB bus from a JSON file")
    return parser

def generate(args):
    s = logging.getLogger("sdb")
    filepath = args.filename[0]
    #If this fails, 
    try:
        f = open(filepath, 'r')
        s.debug("Opened File")
    except IOError as err:
        print ("Filename: %s does not exists!" % filepath)
        sys.exit(0)

    sdb_dict = None
    try:
        sdb_dict = json.load(f, object_pairs_hook = OrderedDict)
        s.debug("Loaded JSON File")
    except ValueError as err:
        print ("Detected an Error in the JSON Configuration file:")
        print (str(err))
        sys.exit(0)

    #Now we have an SDB structure in the form of a Python dictionary
    generate_som(sdb_dict)

def _extract_data(som, root_bus, bus_dict):
    if "interconnects" in bus_dict:
        for bus in bus_dict["interconnects"]:
            som_bus = som.insert_bus(root_bus, bus)
            sub_dict = bus_dict["interconnects"][bus]
            _extract_data(som, som_bus, sub_dict)

    if "devices" in bus_dict:
        for dev in bus_dict["devices"]:
            #print ("dev index: %s" % str(dev))
            component = sdb_component.create_device_record(name = dev)
            c_dict = bus_dict["devices"][dev]
            ###: XXX REALLY BAD PROGRAMMING PRACTICE, THIS NEEDS TO CHANGE!!
            if "abi_class" in c_dict:
                component.d["SDB_ABI_CLASS"] = c_dict["abi_class"]
        
            if "abi_ver_major" in c_dict:
                component.d["SDB_ABI_VERSION_MAJOR"] = hex(c_dict["abi_ver_major"])
        
            if "abi_ver_minor" in c_dict:
                component.d["SDB_ABI_VERSION_MINOR"] = hex(c_dict["abi_ver_minor"])
        
            if "version" in c_dict:
                component.d["SDB_CORE_VERSION"] = c_dict["version"]
        
            if "vendor_id" in c_dict:
                component.d["SDB_VENDOR_ID"] = c_dict["vendor_id"]
        
            if "component.d_id" in c_dict:
                component.d["SDB_DEVICE_ID"] = c_dict["component.d_id"]
        
            if "date" in c_dict:
                component.d["SDB_DATE"] = c_dict["date"]
        
            if "version" in c_dict:
                component.d["SDB_CORE_VERSION"] = c_dict["version"]

            som.insert_component(root_bus, component)
            if "size" in c_dict:
                size = int(c_dict["size"], 0)
                component.set_size(size)


    if "integration" in bus_dict:
        for info in bus_dict["integration"]:
            c_dict = bus_dict["integration"][info]
            component = sdb_component.create_integration_record(information = info)
            if "vendor_id" in c_dict:
                component.d["SDB_VENDOR_ID"] = hex(int(c_dict["vendor_id"], 0))
        
            if "device_id" in c_dict:
                component.d["SDB_DEVICE_ID"] = hex(int(c_dict["device_id"], 0))
        
            if "date" in c_dict:
                component.d["SDB_DATE"] = c_dict["date"]
            som.insert_component(root_bus, component)

    if "repo_url" in bus_dict:
        component = sdb_component.create_repo_url_record(bus_dict["repo_url"])
        som.insert_component(root_bus, component)

    if "synthesis" in bus_dict:
        c_dict = bus_dict["synthesis"]
        component = sdb_component.create_synthesis_record(synthesis_name = c_dict["syn_name"],
                                commit_id = c_dict["commit_id"],
                                tool_name = c_dict["tool_name"],
                                tool_version = c_dict["tool_version"],
                                user_name = c_dict["user_name"])
        som.insert_component(root_bus, component)
 


def generate_som(sdb_dict):
    s = logging.getLogger("sdb")
    s.debug("Generating SDB Object Model")
    som = sdb_object_model.SOM()
    som.initialize_root()

    #Get the root bus name
    #print "SDB: %s" % str(sdb_dict)
    root_name = list(sdb_dict.keys())[0]
    root = som.get_root()
    som.set_bus_name(root, root_name)
    _extract_data(som, root, sdb_dict[root_name])
    som.pretty_print_sdb()


