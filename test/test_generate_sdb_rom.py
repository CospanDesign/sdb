#! /usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),
                             os.pardir))

from sdb import sdb_object_model
from sdb import sdb_component

class Test (unittest.TestCase):
    """Unit Test"""

    def setUp(self):
        pass

    def xtest_simple_flat_bus(self):
        print ("Test create a SOM with one device")
        som = sdb_object_model.SOM()
        som.initialize_root()

        root_name = "top"
        root = som.get_root()
        som.set_bus_name(root, root_name)

        #Put data into SOM

        #Create a device
        component = sdb_component.create_device_record("device1")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "1"
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/26"
        component.set_size(0x100)   #256 bytes long

        som.insert_component(root, component)

        som.pretty_print_sdb()

    def xtest_simple_sub_bus(self):
        print ("Test create a SOM with a bus and a device within that bus")
        som = sdb_object_model.SOM()
        som.initialize_root()

        root_name = "top"
        root = som.get_root()
        som.set_bus_name(root, root_name)

        #Put data into SOM
        #Create a bus
        bus_name = "peripherals"
        bus = som.insert_bus(root, bus_name)    #Need to the bus under another bus

        #Create a device
        component = sdb_component.create_device_record("device1")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "2"  #Thees numbers are defined in 'sdb/data/local_devices/devices.json'
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/26"
        component.set_size(0x100)   #256 bytes long

        som.insert_component(bus, component)

        som.pretty_print_sdb()


    def xtest_two_buses(self):
        print ("Two buses")

        #By disabling auto-address user will need to specify all address
        som = sdb_object_model.SOM(auto_address = False)
        som.initialize_root()

        root_name = "top"
        root = som.get_root()
        som.set_bus_name(root, root_name)

        #Put data into SOM
        #Create a bus
        bus_name = "peripherals"
        periph_bus = som.insert_bus(root, bus_name)    #Need to the bus under another bus

        bus_name = "memory"
        mem_bus = som.insert_bus(root, bus_name)    #Need to the bus under another bus
        #Explicitly specify the address of the memory
        mem_bus.get_component().set_start_address(0x100000000)
        #By default the memory bus will be put at the end of the peripheral but the address can be explicitly set


        #Put elements into the memory bus
        component = sdb_component.create_device_record("memory0")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "6"  #Thees numbers are defined in 'sdb/data/local_devices/devices.json'
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/25"
        component.set_start_address(0x0000)
        component.set_size(0x10000)   #256 bytes long

        som.insert_component(mem_bus, component)



        #Create a device
        component = sdb_component.create_device_record("device0")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "2"  #Thees numbers are defined in 'sdb/data/local_devices/devices.json'
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/26"
        component.set_start_address(0x001000)
        component.set_size(0x100)   #256 bytes long

        som.insert_component(periph_bus, component)

        component = sdb_component.create_device_record("device1")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "3"  #Thees numbers are defined in 'sdb/data/local_devices/devices.json'
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/26"
        component.set_start_address(0x002000)
        component.set_size(0x10000)   #256 bytes long

        som.insert_component(periph_bus, component)

        som.pretty_print_sdb()


    def test_complex_buses(self):
        print ("Complex buses")

        #By disabling auto-address user will need to specify all address
        som = sdb_object_model.SOM(auto_address = False)
        som.initialize_root()

        root_name = "top"
        root = som.get_root()
        som.set_bus_name(root, root_name)

        #Put data into SOM
        #Create a bus
        bus_name = "peripherals"
        periph_bus = som.insert_bus(root, bus_name)    #Need to the bus under another bus

        bus_name = "memory"
        mem_bus = som.insert_bus(root, bus_name)    #Need to the bus under another bus
        #Explicitly specify the address of the memory
        mem_bus.get_component().set_start_address(0x100000000)
        #By default the memory bus will be put at the end of the peripheral but the address can be explicitly set


        #Put elements into the memory bus
        component = sdb_component.create_device_record("memory0")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "6"  #Thees numbers are defined in 'sdb/data/local_devices/devices.json'
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/25"
        component.set_start_address(0x0000)
        component.set_size(0x10000)   #256 bytes long

        som.insert_component(mem_bus, component)

        #Put elements into the memory bus
        component = sdb_component.create_device_record("memory1")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "6"  #Thees numbers are defined in 'sdb/data/local_devices/devices.json'
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/25"
        component.set_start_address(0x10100)
        component.set_size(0x20000)   #256 bytes long


        som.insert_component(mem_bus, component)



        #Create a device
        component = sdb_component.create_device_record("device0")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "2"  #Thees numbers are defined in 'sdb/data/local_devices/devices.json'
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/26"
        component.set_start_address(0x001000)
        component.set_size(0x100)   #256 bytes long

        som.insert_component(periph_bus, component)

        component = sdb_component.create_device_record("device1")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "3"  #Thees numbers are defined in 'sdb/data/local_devices/devices.json'
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/26"
        component.set_start_address(0x002000)
        component.set_size(0x10000)   #256 bytes long

        som.insert_component(periph_bus, component)

        som.pretty_print_sdb()



    def test_complex_buses_with_info(self):
        print ("Complex buses")

        #By disabling auto-address user will need to specify all address
        som = sdb_object_model.SOM(auto_address = False)
        som.initialize_root()

        root_name = "top"
        root = som.get_root()
        som.set_bus_name(root, root_name)




        synth = sdb_component.create_synthesis_record(
                                        synthesis_name = "my_project.bit",
                                        commit_id = 12345,
                                        tool_name = "vivado",
                                        tool_version = "2016.4",
                                        user_name = "billybobob")

        som.insert_component(root, synth)

        url_repo = sdb_component.create_repo_url_record("http://www.example.com")
        som.insert_component(root, url_repo)

        #Put data into SOM
        #Create a bus
        bus_name = "peripherals"
        periph_bus = som.insert_bus(root, bus_name)    #Need to the bus under another bus

        bus_name = "memory"
        mem_bus = som.insert_bus(root, bus_name)    #Need to the bus under another bus
        #Explicitly specify the address of the memory
        mem_bus.get_component().set_start_address(0x100000000)
        #By default the memory bus will be put at the end of the peripheral but the address can be explicitly set


        #Put elements into the memory bus
        component = sdb_component.create_device_record("memory0")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "6"  #Thees numbers are defined in 'sdb/data/local_devices/devices.json'
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/25"
        component.set_start_address(0x0000)
        component.set_size(0x10000)   #256 bytes long

        som.insert_component(mem_bus, component)

        #Put elements into the memory bus
        component = sdb_component.create_device_record("memory1")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "6"  #Thees numbers are defined in 'sdb/data/local_devices/devices.json'
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/25"
        component.set_start_address(0x10100)
        component.set_size(0x20000)   #256 bytes long


        som.insert_component(mem_bus, component)



        #Create a device
        component = sdb_component.create_device_record("device0")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "2"  #Thees numbers are defined in 'sdb/data/local_devices/devices.json'
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/26"
        component.set_start_address(0x001000)
        component.set_size(0x100)   #256 bytes long

        som.insert_component(periph_bus, component)

        component = sdb_component.create_device_record("device1")
        component.d["SDB_ABI_CLASS"] = "0"
        component.d["SDB_ABI_VERSION_MAJOR"] = "3"  #Thees numbers are defined in 'sdb/data/local_devices/devices.json'
        component.d["SDB_ABI_VERSION_MINOR"] = "1"
        component.d["SDB_CORE_VERSION"] = "00.000.001"
        component.d["SDB_VENDOR_ID"] = "0x0001"
        component.d["SDB_DEVICE_ID"] = "0x0001"
        component.d["SDB_DATE"] = "2017/02/26"
        component.set_start_address(0x002000)
        component.set_size(0x10000)   #256 bytes long

        som.insert_component(periph_bus, component)

        som.pretty_print_sdb()






if __name__ == "__main__":
    unittest.main()
