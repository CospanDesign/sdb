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
import json
from sdb_component import SDBError
from collections import OrderedDict as odict

__author__ = "dave.mccoy@cospandesign.com (Dave McCoy)"

'''
Functions to manage devices
'''

LOCAL_DEVICE_LIST = os.path.join(os.path.dirname(__file__), "data", "local_devices", "devices.json")
LOCAL_DEVICE_LIST = os.path.abspath(LOCAL_DEVICE_LIST)


def get_device_list():
    """Return a list of device names where the index corresponds to the device
    identification number

    Args:
      Nothing

    Returns:
      (list): List of devices
          (index corresponds to devices identification number)

    Raises:
      Nothing
    """
    dev_tags = {}
    dev_list = []
    index = 0
    length = 0
    try:
        f = open(LOCAL_DEVICE_LIST, "r")
        sdb_tags = json.load(f, object_pairs_hook = odict)
    except TypeError as err:
        print ("JSON Error: %s" % str(err))
        raise SDBError("DRT Error: %s", str(err))

    dev_tags = sdb_tags["devices"]

    length = len(dev_tags.keys())

    int_dict = {}
    for key in dev_tags:
        #change the hex number into a integer
        index = None
        id_val = dev_tags[key]["ID"]
        if isinstance(id_val, str) or isinstance(id_val, unicode):
            index = int(id_val[2:], 16)
        else:
            index = id_val

        dev_tags[key]["name"] = key
        #print "index: %d" % index
        int_dict[index] = dev_tags[key]

    ordered_keys = int_dict.keys()
    dev_list = []
    for key in ordered_keys:
        dev_list.append(int_dict[key])

    return dev_list

def get_device_name_from_id(device_id):
    """return device name for the ID

    Args:
        ID (int): device id number

    Return:
        name (string): name of the device

    Raises:
        Nothing
    """
    #print "Index: 0x%04X" % device_id
    dev_tags = {}
    try:
        f = open(LOCAL_DEVICE_LIST, "r")
        sdb_tags = json.load(f)
    except TypeError as err:
        print ("JSON Error: %s" % str(err))
        raise SDBError("DRT Error: %s", str(err))

    dev_tags = sdb_tags["devices"]
    did = 0
    for device in dev_tags:
        #print "Looking at: %s" % device
        did = None
        if (type(dev_tags[device]["ID"]) == str) or (type(dev_tags[device]["ID"]) == unicode):
            did = int(dev_tags[device]["ID"], 16)
        else:
            did = dev_tags[device]["ID"]

        if did == device_id:
            return device
    return "Unknown Device"

def get_device_id_from_name(name):
    """return the index of the device speicified by name
    The name can be found in the devices.json file
    Example: if name == GPIO, then 2 will be returned

    Args:
      name (string): name of the core to identify

    Return:
      device identification number

    Raises:
      Nothing

    """
    dev_tags = {}
    try:
        f = open(LOCAL_DEVICE_LIST, "r")
        sdb_tags = json.load(f)
    except TypeError as err:
        print ("JSON Error: %s" % str(err))
        raise SDBError("DRT Error: %s", str(err))

    dev_tags = sdb_tags["devices"]
    for key in dev_tags:
        if name.lower().strip() == key.lower().strip():
            name = key

    if name not in dev_tags.keys():
        raise SDBError("Name: %s is not a known type of devices" % name)

    return int(dev_tags[name]["ID"], 0)


def get_device_type(index):
    """return the name of the device referenced by index

    Args:
        index (int): Integer of device index

    Return:
        (string) Name of the device

    Raises:
        Nothing
    """
    dev_list = get_device_list()
    return dev_list[index]["name"]


