###############################################################
# ble_network_control.py	                                  #
# author:   Frank Arts                                        #
# date:     October 23th, 2020                   		      #
# version 1.0												  #
#                                                             #
# version info:                                               #
# - Add dictionary with my ble names (services and tasks)     #
# - Add BLE_network class to adjust and control a ble network #
# - Add function to get name of ble serive/task from bluepy   #
#   or from my dictionary                                     #
# - Add function to scan for ble devices                      #
# - Add function to print services and tasks                  #
#                                                             #
# NOTES:											          #
# - Mesh networks are not supported                           #
# - Reading from tasks is not yet supported                   #
# - Writing to tasks is not yet supported                     #
###############################################################

# import
from bluepy.btle import Scanner, DefaultDelegate, Service
from bluepy.btle import UUID, Peripheral, AssignedNumbers
from bluepy.btle import ADDR_TYPE_PUBLIC, ADDR_TYPE_RANDOM
import sys, binascii

###################
## my dictionary ##
###################

# my dictionary of uuids (services and tasks)
my_ble_names = {
    ## Services ##
    # UUID                                  Service name
    "00001523-1212-efde-1523-785feabcd123": "Button service",
    "00001623-1212-efde-1523-785feabcd123": "LED service",
    
    
    ## Tasks/Characteristics ##
    # UUID                                  Taks name
    "00001524-1212-efde-1523-785feabcd123": "Button task",
    "00001624-1212-efde-1523-785feabcd123": "LED task",
}


###############
### Classes ###
###############

# Class to save devices
class _ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device %s" % dev.addr)
        elif isNewData:
            print("Received new data from %s" % dev.addr)


class BLE_network:
    """
    BLE network class
    < UNDER DEVELOPMENT >
    This class contains of one or multiple peripherals (= node = profile)
    These peripherals should be gathered using the bluepy library (https://github.com/IanHarvey/bluepy)
    
    ...
    
    attributes
    ----------
    All attributes below are read-only.
    - ID
        Network ID
    
    methods
    -------
    - peripherals
    add_peripherals(self, peripheral)
        Add one or mutliple peripherals
        peripheral must be of type Peripheral (one) or list (one or multiple)
    
    delete_peripherals(self, peripheral_addr = None)
        Delete all peripherals or specified peripheral(s) with MAC address peripheral_addr
        peripheral_addr must be of type None (all), unicode (one) or list (one or multiple)
   
    get_peripherals(self, peripheral = None)
        Return a list containing the Peripherals of all peripherals or specified peripheral(s)
        peripheral must be of type None (all), Periperheral (one) or list (one or multiple)
    
    get_addresses(self, peripheral_addr = None)
        Return a list containing the addresses of all peripherals or specified peripheral(s)
        peripheral_addr must be of type None (all), unicode (one) or list (one or multiple)
    
    
    - task control
    read_task(self, peripheral_addr, service_uuid, task_uuid)
        Read one or multiple tasks
        Write 'value' to one or multiple peripherals
        peripheral_addr must be of type unicode (one) or list (one or multiple)
        service_uuid and task_uuid must be of type str (one) or list (one or multiple)
        return value will be the same type as task (i.e. int, float, str)
        < NOTE: Not implemented yet >

    write_task(self, peripheral_addr, service_uuid, task_uuid, value)
        Write 'value' to one or multiple tasks
        peripheral_addr must be of type unicode (one) or list (one or multiple)
        service_uuid and task_uuid must be of type str (one) or list (one or multiple)
        value must be the same type as task (i.e. int, float, str)
        < NOTE: Not implemented yet >
    
    ------

    """
    
    # attributes #
    @property
    def netID(self):
        '''Network ID'''
        return self.__netID
    
    
    # consturctor #
    def __init__(self, network_ID, peripheral = None):
        '''Initialize a dictionary of peripherals.
       network_ID should not be of type None. Any other type is acceptable.
       peripheral must be of type None, Peripheral, or list of Peripheral'''
        if (peripheral is None):
            self.__netID = network_ID
            self.__peripherals = {}
            print("Created network with network ID: '%s'" %self.netID)
            print("    Empty dictionary of peripherals has been created")
        elif (isinstance(peripheral, Peripheral) or isinstance(peripheral, list)):
            self.__netID = network_ID
            print("Created network with network ID: '%s'" %self.netID)
            
            self.__peripherals = {}
            self.add_peripherals(peripheral)
        else:
            print("ERROR while trying to add peripherals: peripheral is of wrong type (type = %s). Valid types: None, Peripheral, list (of Peripheral)" %type(peripheral))
        
        print('')
    
    # destructor
    def __del__(self):
        '''Delete network with ID x.'''
        print("BLE network '%s' has been deleted." %self.netID)
    
    # methods #
    def add_peripherals(self, peripheral):
        '''Add one or mutliple peripherals
        peripheral must be of type Peripheral (one) or list (one or multiple)'''
        if (isinstance(peripheral, Peripheral)):
            no_repeat = False
            no_repeat = self.__peripherals.get(peripheral.addr, True)
            self.__peripherals[peripheral.addr] = peripheral
            
            print("Added a peripheral to network with network ID: '%s'" %self.netID)
            if (no_repeat == True):
                print("    [new] Added peripheral has MAC address: %s" %peripheral.addr)
            else:
                print("    [update] Updated peripheral has MAC address: %s" %peripheral.addr)
        elif (isinstance(peripheral, list)):
            print("Added peripherals to network with network ID: '%s'" %self.netID)
            for i in range(len(peripheral)):
                no_repeat = False
                no_repeat = self.__peripherals.get(peripheral[i].addr, True)
                self.__peripherals[peripheral[i].addr] = peripheral[i]
                
                if (no_repeat == True):
                    print("    [new] Added peripheral has MAC address: %s" %peripheral[i].addr)
                else:
                    print("    [update] Updated peripheral has MAC address: %s" %peripheral[i].addr)
        else:
            print("ERROR while trying to add peripherals: peripheral is of wrong type (type = %s). Valid types: Peripheral, list (of Peripheral)" %type(peripheral))
        
        print('')
    
    def delete_peripherals(self, peripheral_addr = None):
        '''Delete all peripherals or specified peripheral(s) with MAC address peripheral_addr
        peripheral_addr must be of type unicode (one) or list (one or multiple)'''
        if (peripheral_addr == None):
            self.__peripherals.clear()
            print("Deleted all peripherals from this network")
        elif (isinstance(peripheral_addr, unicode)):
            not_in_list = self.__peripherals.pop(peripheral_addr, True)
            if (not_in_list is not True):
                print("Deleted peripheral with MAC address %s from network" %peripheral_addr)
            else:
                print("peripheral with MAC address %s is not part of this network (network ID = %s)" %(peripheral_addr, self.netID))
        elif (isinstance(peripheral_addr, list)):
            for i in range(len(peripheral_addr)):
                not_in_list = self.__peripherals.pop(peripheral_addr[i], True)
                if (not_in_list is not True):
                    print("Deleted peripheral with MAC address %s from network" %peripheral_addr[i])
                else:
                    print("peripheral with MAC address %s is not part of this network (network ID = %s)" %(peripheral_addr[i], self.netID))
        else:
            print("ERROR while trying to delete peripherals: peripheral is of wrong type (type = %s). Valid types: None, Peripheral, dict (of Peripheral)" %type(peripheral))
        
        print('')
    
    def get_peripherals(self, peripheral_addr = None):
        '''Return a list containing the Peripherals of all peripherals or specified peripheral(s)
        peripheral must be of type None (all), unicode (one) or list (one or multiple)'''
        p = []
        
        if (peripheral_addr == None):
            p = self.__peripherals.values()
        elif (isinstance(peripheral_addr, unicode)):
            val = self.__peripherals.get(peripheral_addr, "not in list")
            if (val == "not in list"):
                print("peripheral with MAC address %s is not part of this network (network ID = %s)" %s(peripheral_addr, self.netID))
            else:
                p.append(val)
        elif (isinstance(peripheral_addr, list)):
            for i in range(len(peripheral_addr)):
                val = self.__peripherals.get(peripheral_addr[i], "not in list")
                if (val == "not in list"):
                    print("peripheral with MAC address '%s' is not part of this network (network ID = %s)" %s(peripheral_addr[i], self.netID))
                else:
                    p.append(val)
        else:
            print("ERROR while trying to get peripherals: peripheral is of wrong type (type = %s). Valid types: None, unicode, list (of unicode)" %type(peripheral))
        
        return p
    
    def get_addresses(self, peripheral_addr = None):
        '''Return a list containing the addresses of all peripherals or specified peripheral(s)
        peripheral_addr must be of type unicode (one) or list (one or multiple)'''
        addr = []
        
        if (peripheral_addr == None):
            addr = self.__peripherals.keys()
        elif (isinstance(peripheral_addr, unicode)):
            val = self.__peripherals.get(peripheral_addr, "not in list")
            if (val == "not in list"):
                print("peripheral with MAC address %s is not part of this network (network ID = %s)" %s(peripheral_addr, self.netID))
            else:
                addr.append(val.addr)
        elif (isinstance(peripheral_addr, list)):
            for i in range(len(peripheral_addr)):
                val = self.__peripherals.get(peripheral_addr[i], "not in list")
                if (val == "not in list"):
                    print("peripheral with MAC address %s is not part of this network (network ID = %s)" %s(peripheral_addr[i], self.netID))
                else:
                    addr.append(val.addr)
        else:
            print("ERROR while trying to get peripherals: peripheral is of wrong type (type = %s). Valid types: None, unicode, list (of unicode)" %type(peripheral_addr))
        
        return addr
    
    # task control
    def read_task(self, peripheral):
        '''Read one or multiple tasks
        Write 'value' to one or multiple peripherals
        peripheral_addr must be of type unicode (one) or list (one or multiple)
        service_uuid and task_uuid must be of type str (one) or list (one or multiple)
        return value will be the same type as task (i.e. int, float, str)
        < NOTE: Not implemented yet >'''
        print("< Read peripheral is not implemented yet >")
        print('')

    def write_task(self, peripheral, value):
        '''Write 'value' to one or multiple tasks
        peripheral_addr must be of type unicode (one) or list (one or multiple)
        service_uuid and task_uuid must be of type str (one) or list (one or multiple)
        value must be the same type as task (i.e. int, float, str)
        < NOTE: Not implemented yet >'''
        print("< Write peripheral is not implemented yet >")
        print('')



#################
### Functions ###
#################

def getNameByUUID(uuid):
    '''Return the name (str) of a uuid. If the uuid is listed in the bluepy Assigned Numbers list or my_ble_names list it will be a human-readable name. Otherwise, it returns the given uuid (str).
    (bluepy Assignment Numbers (str) can be found here: https://ianharvey.github.io/bluepy-doc/assignednumbers.html#assignednumbers)'''
    return my_ble_names.get(str(uuid), UUID(uuid).getCommonName())


def scan_for_ble_devices(scan_time = 10.0):
    '''Scan all for all ble devices. It returns a list of all found ble devices.'''
    scanner = Scanner().withDelegate(_ScanDelegate())
    sc_devices = scanner.scan(scan_time)    # Scan for specified time (in seconds) default = 10.0 seconds

    # Variables for copies of MAC_addr and device of correct device
    se_device = None
    
    for dev in sc_devices:
        valid_device = False
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))

        # Display all adtype, desc and value of current device
        for (adtype, desc, value) in dev.getScanData():
            print("  %s    %s = %s" % (hex(adtype), desc, value))
            if desc == "Complete Local Name" and value == local_device_name:
                valid_device = True;    # Valid device is found (works only for the first device called "Nordic_Blinky"
                print("Found valid device!")
                se_device = dev

        # save + print correct device address
        if valid_device:
            print("MAC address valid device: %s\n" %  dev.addr)
        else:
            print("Not a valid device!\n")

    return se_device


def print_services_and_tasks(p_device, local_device_name = "Nordic_Blinky"):
    '''Print all services and tasks of a given device. If the task is readable, it is read as well.'''
    # NOTE for c-code: Only displayed when service is advertised (advertising_init() and initialized (services_init()) in nRF52DK's main.c
    
    print('')
    # Print all services
    print("Services and Charactertic uuids of device '%s':" % local_device_name)

    for se_service in p_device.getServices():
        # Print services
        print("Service:")
        uuid = se_service.uuid       # Get uuid
        print(getNameByUUID(uuid))   # Print service name (string)

        # Print tasks
        print("    Tasks:")
        chars = False                # More than 0 tasks?
        for ch_task in se_service.getCharacteristics():    # Create object of task class (for every task in se_ object of service class)
            chars = True
            uuid = ch_task.uuid          # Get uuid
            task_name = getNameByUUID(uuid)
            print("    %s" %task_name)   # Print task name (string)
            print("      (uuid=%s)" %uuid)

            # Show properties:
            print("      %s" %ch_task.propertiesToString())

            # Save device name task
            if (task_name is not uuid):
                if(task_name.lower() == "device name"):
                    if(ch_task.supportsRead()):
                        device_name = ch_task.read()
                    else:
                        print("ERROR: %s is not readable" %ch_task)
                    
            # Read task if it supports read
            if(ch_task.supportsRead()):
                # Task is readable => Read + print value
                str_in = ch_task.read()
                print("        Current value: %s" % binascii.b2a_hex(ch_task.read()))
            else:
                # Not readable
                print("ERROR: %s is not readble" %ch_task)

        if (chars is False):
            print("    n/a")
        print('')
