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

import sdb_component
import device_manager
from sdb_component import SDBComponent as sdbc
from sdb_component import is_valid_bus_type

from sdb_core import SDBInfo
from sdb_core import SDBWarning
from sdb_core import SDBError

DEPTH_SPACE = 4

class SOMComponent(object):

    def __init__(self, parent, c):
        self.parent = parent
        self.c = c

    def get_component(self):
        return self.c

    def get_parent(self):
        return self.parent

    def get_name(self):
        return self.c.get_name()

    def set_name(self, name):
        self.c.set_name(name)

class SOMBus(SOMComponent):

    def __init__(self, parent):
        self.spacing = 0
        self.children = []
        super(SOMBus, self).__init__(parent, sdbc())
        self.c = sdb_component.create_interconnect_record( name = "bus",
                                                  vendor_id = 0x800000000000C594,
                                                  device_id = 0x00000001,
                                                  start_address = 0x00,
                                                  size = 0x00)
        self.curr_pos = 0

    def insert_child(self, child, pos = -1):
        if pos == -1:
            self.children.append(child)
        else:
            self.children.insert(pos, child)
        size = 0
        for child in self.children:
            size += child.c.get_size_as_int()

        #self.c.set_size(size)

    def get_child_from_index(self, i):
        return self.children[i]

    def remove_child_at_index(self, i):
        child = self.children[i]
        self.remove_child(child)

    def remove_child(self, child):
        self.children.remove(child)
        size = 0
        for child in self.children:
            size += child.c.get_size_as_int()

        #self.c.set_size(size)

    def get_child_count(self):
        return len(self.children)

    def is_root(self):
        return False

    def get_component(self):
        return self.c

    def set_child_spacing(self, spacing = 0):
        """
        sets the spacing of the children within a bus, by default this is zero
        which means the children will be put right after each other, however
        if this value is set to a larger number such as 0x01000000 then every
        child start address will start on a 0x01000000 boundary as an example:

        child 0 @ 0x00000000
        child 1 @ 0x01000000
        child 2 & 0x02000000

        Args:
            spacing (integer): start spacing of a child in the bus

        Return:
            Nothing

        Raises:
            Nothing
        """
        #import pdb
        #pdb.set_trace()
        self.spacing = spacing

    def get_child_spacing(self):
        """
        Returns the minimum spacing between children start address

        Args:
            Nothing

        Returns (integer):
            spacing between start address of children

        Raises:
            Nothing
        """
        return self.spacing

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        self.curr_pos = 0
        return self

    def next(self):
        if self.curr_pos == len(self.children):
            raise StopIteration
        pos = self.curr_pos
        self.curr_pos += 1
        return self.children[pos]

class SOMRoot(SOMBus):

    def __init__(self):
        super(SOMRoot, self).__init__(None)
        self.c.d["SDB_NAME"] = "Root"

    def is_root(self):
        return True


#User Facing Object
class SOM(object):

    def __init__(self, auto_address = True):
        self.root = None
        self.reset_som()
        self.current_rot = self.root
        self.current_pos = 0
        self.auto_address = auto_address

    #Bus Functions
    def initialize_root(self,
                                name = "top",
                                version = sdbc.SDB_VERSION,
                                vendor_id = 0x8000000000000000,
                                entity_id = 0x00000000,
                                bus_type = "wishbone"):

        c = self.root.get_component()
        c.d["SDB_NAME"] = name
        if version > sdbc.SDB_VERSION:
            raise SDBError("Version %d is greater than known version! (%d)" %
                            (version,
                            sdbc.SDB_VERSION))
        c.d["SDB_VERSION"] = version

        if not is_valid_bus_type(bus_type):
            raise SDBError("%s is not a valid bus type" % bus_type)
        c.d["SDB_BUS_TYPE"] = "wishbone"

    def get_root(self):
        """
        Returns the root of the bus

        Args:
            Nothing

        Returns:
            (SOMBus): the base bus of the SOM

        Raises:
            Nothing
        """
        return self.root

    def get_buses(self, root = None):
        """
        Returns a list of buses that are underneath the provided root

        Args:
            (SOMBus): The root bus to retrieve the sub buses from

        Returns: (Tuple of SOMBus)

        Raises:
            Nothing
        """
        if root is None:
            root = self.root

        bus_list = []
        for i in range(root.get_child_count()):
            child = root.get_child_from_index(i)
            if isinstance(child, SOMBus):
                bus_list.append(child)


        return tuple(bus_list)

    def is_entity_a_bus(self, root = None, index = None):
        """
        Returns true if the entity at the specified index is a bus

        Args:
            root(SOMBus): The bus where the devcies are
                leave blank for the top of the tree
            index(Integer): The index of the entity within the root bus

        Return (Boolean):
            True: entity is a bus
            False: entity is not a bus

        Raises:
            SDBError:
                index is not supplied
        """
        if index is None:
            raise SDBError("index is None, this should be an integer")

        if root is None:
            root = self.root

        n = root.get_child_from_index(index)
        if isinstance(n, SOMBus):
            return True

        return False

    def insert_bus(self,
                    root = None,
                    name = None,
                    bus = None,
                    pos = -1):
        """
        Add a new bus into the SDB Network, if the user supplies the root
        then the new item will be inserted into the root bus otherwise
        insert it into the bus provided.

        The name of the bus can be set initially or later

        Args:
            root(SOMBus): the bus where this new bus will be added

            name(String): Name of the bus to add, could be left blank
            start_address(integer): where to add this bus relative to the
                above bus
            bus(SOMBus): a SOM Bus this can be used to add a pre-existing bus
            pos(integer): position of where to put bus, leave blank to put it
            at the end

        Return:
            (SOMBus): The branch element returned to the user for
                use in adding more element
        """
        if root is None:
            root = self.root

        if bus is None:
            bus = SOMBus(root)

        c = bus.get_component()

        if name is not None:
            c.d["SDB_NAME"] = name

        #if start_address is not None:
        #    self.c.set_start_address(start_address)

        root.insert_child(bus, pos)
        self._update()
        return bus

    def remove_bus(self, bus):
        """
        Remove a bus from the SOM

        Args:
            bus (SOMBus): bus to remove

        Return (SOMBus):
            An orphaned SOMBus

        Raises:
            SOMError:   User attempted to remove root
                        User attempted to remove non-existent bus
        """
        parent = bus.get_parent()
        if parent is None:
            raise SDBError("Cannot remove root, use reset_som to reset SOM")
        try:
            parent.remove_child(bus)
        except ValueError as ex:
            raise SDBError("Attempted to remove a non-existent bus from a "\
                            "parent bus: Parent Bus: %s, Child Bus: %s" %
                            parent.c.d["SDB_NAME"],
                            bus.c.d["SDB_NAME"])

    def set_bus_name(self, bus, name):
        """
        Names the bus

        Args:
            bus (SOMBus): bus to rename
            name (String): name

        Return:
            Nothing

        Raises:
            SDBError: bus does not exist
        """
        if bus is None:
            raise SDBError("Bus doesn't exist")

        elif not isinstance(bus, SOMBus):
            raise SDBError("Bus is not an SOMBus")

        c = bus.get_component()
        c.set_name(name)

    def get_bus_name(self, bus):
        """
        Returns the name of the bus

        Args:
            bus (SOMBus): bus

        Return:
            Nothing

        Raises:
            SOBError: bus does not exist
        """
        if bus is None:
            raise SDBError("Bus doesn't exist")

        elif not isinstance(bus, SOMBus):
            raise SDBError("Bus is not an SOMBus")

        return bus.get_component().get_name()

    def is_wishbone_bus(self):
        return self.d["SDB_BUS_TYPE"] == "wishbone"

    def is_axi_bus(self):
        return self.d["SDB_BUS_TYPE"] == "axi"

    def is_storage_bus(self):
        return self.d["SDB_BUS_TYPE"] == "storage"

    #Bus Private Functions

    #Component Entity Functions
    def insert_component(self, root = None, component = None, pos = -1):
        """
        insert a new component into a bus, if root is left empty then
        insert this component into the root

        Args:
            root(SOMBus): The bus where this component should
                be located
            component(SDBComponent): the element in which to add this
                component into
                This component can only be a entity, or informative item
            pos(integer): the location where to put the component, leave blank
                for the end

        Return
            (SOMComponent): the generated SOMComponent is already inserted into
            the tree

        Raises:
            Nothing
        """
        if root is None:
            #print "root is None, Using base root!"
            root = self.root
        else:
            #print "Using custom root..."
            #print ""
            #print ""
            pass

        #Extrapolate the size of the component
        if component.is_interconnect() or component.is_bridge():
            raise SDBError("Only component can be inserted, not %s", component)

        leaf = SOMComponent(root, component)
        root.insert_child(leaf, pos)
        self._update()

    def get_component(self, root = None, index = None):
        """
        Returns a component that represents an SDB Component

        This does not return interconnects or bridges

        Args:
            root (SOMBus): bus for the entitys
                leave blank for the top of the tree

        Return (SDBComponent): Returns the comopnent
            at the index specified on the specified bus

        Raises:
            None
        """
        if root is None:
            root = self.root

        child = root.get_child_from_index(index)
        component = child.get_component()
        return component

    def remove_component_by_index(self, root = None, index = -1):
        """
        Removes a component given it's root and index

        Args:
            root (SOMBus): bus for the entity, leave blan for root
            index (integer): index of item on bus

        Returns:
            Nothing

        Raises:
            ValueError: Component not found
        """
        if root is None:
            root = self.root

        child = root.get_child_from_index(index)
        return self._remove_component(child)

    def move_component(self, from_root, from_index, to_root, to_index):
        """
        Move a component to another location in the SDB

        Args:
            from_root (SOMBus): bus where the component is located
            from_index (integer): index of where to get the item
            to_root (SOMBus): bus where to put the component
            to_index (integer): index of where to put the item

        Returns:
            Nothing

        Raises:
            Value Error: Component not found
        """
        som_component = self.remove_component_by_index(from_root, from_index)
        component = som_component.get_component()
        self.insert_component(to_root, component, to_index)

    #Component Private Functions
    def _remove_component(self, som_component):
        """
        Remove a component from the SOM

        Args:
            component (SDBComponent)

        Returns:
            Nothing

        Raises:
            ValueError: Not found in bus
        """
        parent = som_component.get_parent()
        parent.remove_child(som_component)
        self._update()
        return som_component

    #Utility Functions
    def reset_som(self):
        self.root = SOMRoot()

    def get_child_count(self, root = None):
        """
        Return a count of the children of a specified node

        Args:
            root(SOMBus): the bus where the entitys are
                leave blank for the top of the tree

        Return (integer): number of entitys in a bus

        Raises:
            Nothing
        """
        if root is None:
            root = self.root

        return root.get_child_count()

    def set_bus_component(self, bus, component):
        """
        Replace the internal SDB Component for a BUS

        This is usefull when parsing a ROM

        Args:
            bus (SOMBus): Bus in which to replace the component
            component (SDBComponent): Replacement Component

        Returns:
            Noting

        Raises:
            Nothing
        """
        bus.c = component
        self._update()

    def set_child_spacing(self, bus, spacing):
        """
        Set the spacing for the given bus

        This is used to logically sperate devices on a bus

        Args:
            bus (SOMBus): Bus in which to change spacing
            spacing (Long): Difference between to devices
        """
        bus.set_child_spacing(spacing)
        self._update()

    #Private Functions
    def _update(self, root = None):
        """
        Go through the entire tree updating all buses with the appropriate sizes
        from all the elements

        Args:
            Nothing

        Return:
            Nothing

        Raises:
            Nothing
        """
        if root is None:
            root = self.root
        else:
            #print "Updating root that is not base!"
            #print ""
            #print ""
            pass


        bus_size = 0
        rc = root.get_component()
        start_address = rc.get_start_address_as_int()
        #print ("Root: %s: Start: 0x%08X" % (root.c.get_name(), start_address))
        spacing = root.get_child_spacing()

        '''
        #Bubble sort everything
        for i in range(root.get_child_count()):
            prev_child = None
            for j in range(root.get_child_count()):
                child = root.get_child_from_index(j)
                if prev_child is None:
                    prev_child = child
                    continue
                if child.c.get_start_address_as_int() < prev_child.c.get_start_address_as_int():
                    #print "Reordering children"
                    root.remove_child_at_index(j)
                    root.insert_child(child, j - 1)

                prev_child = child

        print "Sorted Children:"
        for i in range(root.get_child_count()):
            child = root.get_child_from_index(i)
            print "\tchild %s: 0x%02X" % (child.c.d["SDB_NAME"], child.c.get_start_address_as_int())
        '''

        #Move all informative elements to the end of the bus
        #Bubble sort all non informative elements to the front of informative
        #   elements
        for i in range(root.get_child_count()):
            prev_child = None
            for j in range(root.get_child_count() - 1, -1, -1):
                child = root.get_child_from_index(j)
                if prev_child is None:
                    prev_child = child
                #print "Comparing..."
                #print "child is an integration record: %s" % str(child.c.is_integration_record())
                if  child.c.is_integration_record() or child.c.is_synthesis_record() or child.c.is_url_record():
                    root.remove_child_at_index(j)
                    root.insert_child(child, j + 1)

                prev_child = child

        #Adjust all the sizes for the busses
        prev_child = None
        for i in range(root.get_child_count()):
            child = root.get_child_from_index(i)
            c = child.get_component()
            #print ("Child Name: %s" % c.get_name())
            if prev_child is None:
                #print ("First Item")
                #print ("Address: %08X" % c.get_start_address_as_int())
                #First child should always be 0 relative to this bus

                if self.auto_address:
                    c.set_start_address(0x00)
                prev_child = child
                if isinstance(child, SOMBus):
                    #print "Found bus, initate recursive update"
                    self._update(child)

                #Bus Size
                #bus_size = c.get_start_address_as_int() + c.get_size_as_int()
                #print "bus size: 0x%08X" % bus_size
                if self.auto_address:
                    if spacing == 0:
                        bus_size += c.get_size_as_int()
                    else:
                        mul = (c.get_size_as_int() / spacing) + 1
                        bus_size += mul * spacing

                else:
                    bus_size = c.get_start_address_as_int() + c.get_size_as_int()

                continue

            pc = prev_child.get_component()
            spacing_size = 0
            if isinstance(child, SOMBus):
                #print "Found bus, initate recursive update"
                self._update(child)

            prev_start_address = pc.get_start_address_as_int()
            prev_child_size = pc.get_size_as_int()

            #Add an extra spacing size so that all divided values will at least
            #be one
            spacing_size = prev_child_size
            if spacing > 0:
                mul = (prev_child_size / spacing) + 1
                spacing_size = mul * spacing


            current_start_address = c.get_start_address_as_int()
            new_child_start_address = prev_start_address + spacing_size
            if self.auto_address and (current_start_address < new_child_start_address):
                    #print ("New child start address: 0x%016X" % new_child_start_address)
                    c.set_start_address(new_child_start_address)

            prev_child = child

            if spacing == 0:
                bus_size += c.get_size_as_int()
            else:
                mul = (c.get_size_as_int() / spacing) + 1
                bus_size += mul * spacing


        #print "\tbus size: 0x%08X" % bus_size
        if not self.auto_address and root.get_child_count() > 0:
            child = root.get_child_from_index(root.get_child_count() - 1)
            c = child.get_component()
            bus_size = c.get_start_address_as_int() + c.get_size_as_int()

        rc.set_size(bus_size)
        rc.set_number_of_records(root.get_child_count())


        #Debug
        '''
        print "Final Children Order:"
        for i in range(root.get_child_count()):
            child = root.get_child_from_index(i)
            print "\tchild %s: 0x%02X" % (child.c.d["SDB_NAME"], child.c.get_start_address_as_int())
        '''

    def pretty_print_sdb(self):
        root = self.get_root()
        s = self._gen_bus_string(root, 1)
        print (s)

    @staticmethod
    def _add_depth_spacing(depth):
        s = ""
        for i in range(depth):
            for j in range(DEPTH_SPACE):
                s += " "
        return s

    def _gen_url_record_string(self, component, depth):
        s = ""
        s += SOM._add_depth_spacing(depth)
        s += "URL: %s\n" % component.get_url()
        s += "\n"
        return s

    def _gen_synthesis_record_string(self, component, depth):
        s = ""
        s += SOM._add_depth_spacing(depth)
        s += "Synthesis: {0:20} Date: {1:10}\n".format(component.get_name(),
                                                       component.get_date())
        s += SOM._add_depth_spacing(depth + 1)
        s += "Tool: {0:10} {1:6}\n".format(component.get_synthesis_tool_name(),
                                           component.get_synthesis_tool_version())
        s += SOM._add_depth_spacing(depth + 1)
        s += "Commit ID: {0:20}\n".format(component.get_synthesis_commit_id())
        s += SOM._add_depth_spacing(depth + 1)
        s += "User: {0:20}\n".format(component.get_synthesis_user_name())
        s += "\n"
        return s

    def _gen_device_record_string(self, component, depth):
        s = ""
        name = component.get_name()
        major = component.get_abi_version_major_as_int()
        minor = component.get_abi_version_minor_as_int()
        dev_name = device_manager.get_device_name_from_id(major)
        s += SOM._add_depth_spacing(depth)
        s += "Device: {0:20} Type (Major:Minor) ({1:0=2X}:{2:0=2X}): {3:10}\n".format(name,
                                                                                      major,
                                                                                      minor,
                                                                                      dev_name)
        s += SOM._add_depth_spacing(depth + 1)
        s += "Address: 0x{0:0=16X}-0x{1:0=16X} : Size: 0x{2:0=8X}\n".format(component.get_start_address_as_int(),
                                                            component.get_end_address_as_int(),
                                                            component.get_size_as_int())
        s += SOM._add_depth_spacing(depth + 1)
        s += "Vendor:Product: {0:0=16X}:{1:0=8X}\n".format(component.get_vendor_id_as_int(),
                                                           component.get_device_id_as_int())
        s += SOM._add_depth_spacing(depth + 1)
        s += "Version: {0:20}\n".format(component.get_core_version())
        s += "\n"
        return s

    def _gen_integration_record_string(self, component, depth):
        s = ""
        s += SOM._add_depth_spacing(depth)
        s += "Integration: {0:20}\n".format(component.get_name())
        s += SOM._add_depth_spacing(depth + 1)
        s += "Vendor:Product: {0:0=16X}:{1:0=8X}\n".format(component.get_vendor_id_as_int(),
                                                           component.get_device_id_as_int())
        s += "\n"
        return s

    def _gen_bus_string(self, bus, depth = 0):
        s = ""
        c = bus.get_component()
        s += SOM._add_depth_spacing(depth)
        s += "Bus: {0:<10} @ 0x{1:0=16X} : Size: 0x{2:0=8X}\n\n".format(bus.get_name(),
                                                                      c.get_start_address_as_int(),
                                                                      c.get_size_as_int())


        for i in range(bus.get_child_count()):
            c = bus.get_child_from_index(i)
            if self.is_entity_a_bus(bus, i):
                s += self._gen_bus_string(c, depth + 1)
            else:
                c = c.get_component()
                if c.is_url_record():
                    s += self._gen_url_record_string(c, depth + 1)

                if c.is_synthesis_record():
                    s += self._gen_synthesis_record_string(c, depth + 1)

                if c.is_device():
                    s += self._gen_device_record_string(c, depth + 1)

                if c.is_integration_record():
                    s += self._gen_integration_record_string(c, depth + 1)

        s += "\n"
        return s

