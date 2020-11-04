###############################################################
# ble_network_control.py                                      #
# author:   Frank Arts                                        #
# date:     November 4th, 2020                                #
# version:  1.2                                               #
#                                                             #
# version info:                                               #
# - Can no longer search for Short Local Name                 #
# - Update my_ble_names                                       #
# - Change add/delete/get_peripherals() and get_addresses()   #
#   for single peripheral/address (not in a list)             #
# - Remove function _print_services_and_tasks()               #
# - Add duplicate protection                                  #
# - Implement reading tasks                                   #
#                                                             #
# NOTES:                                                      #
# - Mesh networks are not supported                           #
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
    "1a310701-63b2-0795-204f-1dda0100d29d": "Portable Airflow service",
    
    ## Tasks/Characteristics ##
    # UUID                                  Task name
    "1a310702-63b2-0795-204f-1dda0100d29d": "Portable Airflow task",
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
    read_tasks(self, peripheral = None, service_uuid = None, task_uuid = None):
        Read one or multiple tasks of one or multiple peripherals
        peripheral must be of type None (all), Peripheral (one) or list (one or multiple)
        service_uuid and task_uuid must be of type None (all), str (one) or list (one or multiple)
        type of return value depends on the task'

    write_tasks(self, value, peripheral_addr = None, service_uuid = None, task_uuid = None)
        Write 'value' to all, one or multiple tasks of one or multiple peripherals
        value must be the same type as task (i.e. int, float, str)
        peripheral_addr must be of type None, unicode (one) or list (one or multiple)
        service_uuid and task_uuid must be of type None, str (one) or list (one or multiple)
        < NOTE: Not implemented yet >
        
    __save_tasks(self, peripheral, service_uuid = None, task_uuid = None):
        Save tasks in the memory (currently only printed for debug purposes)
        peripheral must be of type Peripheral
        service_uuid and task_uuid must be of type None (all), str (one) or list (one or multiple)
        Note: When a service/task is not part of the current peripheral/service, it is ignored.
    
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
        return
    
    # destructor
    def __del__(self):
        '''Delete network with ID x.'''
        print("BLE network '%s' has been deleted." %self.netID)
        return
    
    # methods #
    def add_peripherals(self, peripheral):
        '''Add one or mutliple peripherals
        peripheral must be of type Peripheral (one) or list (one or multiple)'''
        # Convert to list
        if (isinstance(peripheral, Peripheral)):
            peripheral = [peripheral]
            
            
        # Add
        if (isinstance(peripheral, list)):
            # Remove duplicates
            peripheral = list(dict.fromkeys(peripheral))
            
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
        return
    
    def delete_peripherals(self, peripheral_addr = None):
        '''Delete all peripherals or specified peripheral(s) with MAC address peripheral_addr
        peripheral_addr must be of type unicode (one) or list (one or multiple)'''
        
        # Convert to list
        if (isinstance(peripheral_addr, unicode)):
            peripheral_addr = [peripheral_addr]
            
            
        # Delete
        if (peripheral_addr == None):
            # Remove duplicates
            peripheral_addr = list(dict.fromkeys(peripheral_addr))
            
            self.__peripherals.clear()
            print("Deleted all peripherals from this network")
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
        return
    
    def get_peripherals(self, peripheral_addr = None):
        '''Return a list containing the Peripherals of all peripherals or specified peripheral(s)
        peripheral must be of type None (all), unicode (one) or list (one or multiple)'''
        p = []
                
        # Convert to list
        if (isinstance(peripheral_addr, unicode)):
            peripheral_addr = [peripheral_adddr]
            
        
        # Get
        if (peripheral_addr == None):
            p = self.__peripherals.values()
        elif (isinstance(peripheral_addr, list)):
            # Remove duplicates
            peripheral_addr = list(dict.fromkeys(peripheral_addr))
            
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
                
        # Convert to list
        if (isinstance(peripheral_addr, unicode)):
            peripheral_addr = [peripheral_addr]
            
        
        # Get
        if (peripheral_addr == None):
            addr = self.__peripherals.keys()
        elif (isinstance(peripheral_addr, list)):
            # Remove duplicates
            peripheral_addr = list(dict.fromkeys(peripheral_addr))
            
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
    def read_tasks(self, peripheral = None, service_uuid = None, task_uuid = None):
        '''Read one or multiple tasks of one or multiple peripherals
        peripheral must be of type None (all), Peripheral (one) or list (one or multiple)
        service_uuid and task_uuid must be of type None (all), str (one) or list (one or multiple)
        type of return value depends on the task'''
                
        # Convert to list
        if peripheral is None:
            peripheral = [];
            for key, value in self.__peripherals.items():
                peripheral.append(value)
        elif isinstance(peripheral, Peripheral):
            peripheral = [peripheral]
            
        
        # Read
        if (isinstance(peripheral, list)):
            # Remove duplicates
            peripheral = list(dict.fromkeys(peripheral))
            
            for i in range(len(peripheral)):
                addr = self.__peripherals.get(peripheral[i].addr, "not in list")
                if (addr == "not in list"):
                    print("peripheral with MAC address %s is not part of this network (network ID = %s)" %s(peripheral[i].addr, self.netID))
                    print("task(s) for this peripheral will not be read")
                else:
                    # read tasks
                    self.__save_tasks(peripheral[i], service_uuid, task_uuid)
        else:
            print("ERROR while trying to save tasks: wrong type for peripheral (type = %s) or services (type = %s) or tasks (type = %s). Valid type for peripheral: None, Peripheral or list, valid types for services and tasks: list, None" %(type(peripheral), type(services), type(tasks)))
        
        print('')
        return

    def write_tasks(self, value, peripheral_addr = None, service_uuid = None, task_uuid = None):
        '''Write 'value' to one or multiple tasks of one or multiple peripherals
        value must be the same type as task (i.e. int, float, str)
        peripheral_addr must be of type None (all), unicode (one) or list (one or multiple)
        service_uuid and task_uuid must be of type None (all), str (one) or list (one or multiple)
        < NOTE: Not implemented yet >'''
        print("< Write peripheral is not implemented yet >")
        print('')
        
        return
    
    def __save_tasks(self, peripheral, service_uuid = None, task_uuid = None):
        '''Save tasks in the memory (currently only printed for debug purposes)
        peripheral must be of type Peripheral
        service_uuid and task_uuid must be of type None (all), str (one) or list (one or multiple)
        Note: When a service/task is not part of the current peripheral/service, it is ignored.'''
        
        # Convert to list
        if service_uuid == None:
            service_uuid = []
            for service in self.__peripherals[peripheral.addr].getServices():
                service_uuid.append(service.uuid)
        elif isinstance(service_uuid, str):
            service_uuid = [service_uuid]
        
        # Convert to list
        if task_uuid == None:
            task_uuid = []
            for task in self.__peripherals[peripheral.addr].getCharacteristics():
                task_uuid.append(task.uuid)
        elif isinstance(task_uuid, str):
            task_uuid = [task_uuid]
        
        
        if (not isinstance(peripheral, Peripheral) and not isinstance(services, list) and not isinstance(tasks, list)):
            print("ERROR while trying to save tasks: wrong type for peripheral (type = %s) or services (type = %s) or tasks (type = %s). Valid type for peripheral: Peripheral, valid types for services and tasks: list" %(type(peripheral), type(services), type(tasks)))
            return
        
        # Remove duplicates
        service_uuid = list(dict.fromkeys(service_uuid))
        task_uuid    = list(dict.fromkeys(task_uuid))
        
            
        print('')
        # Print specified services
        print("Services and Charactertic uuids of device '%s':" % peripheral.addr)

        
        # Save services
        for se_service in peripheral.getServices():
            if (se_service.uuid not in service_uuid):
                continue;    # Skip this sevice
            
            chars = False                # More than 0 tasks?
            firstTask = True             # Fisrt task?
            
            # Save tasks
            for ch_task in se_service.getCharacteristics():    # Create object of task class (for every task in se_ object of service class)
                chars = True
                
                if (ch_task.uuid not in task_uuid):
                    continue;    # Skip this task
                
                if firstTask:
                    # Print services
                    print("Service:")
                    uuid = se_service.uuid       # Get uuid
                    print(getNameByUUID(uuid))   # Print service name (string)
                    print("(uuid=%s)" %uuid)     # Print uuid

                    print("    Tasks:")
                    firstTask = False
                
                uuid = ch_task.uuid          # Get uuid
                task_name = getNameByUUID(uuid)
                print("    %s" %task_name)   # Print task name (string)
                print("      (uuid=%s)" %uuid)
                
                
                # Show properties:
                print("      %s" %ch_task.propertiesToString())
                        
                # Read task if it supports read
                if(ch_task.supportsRead()):
                    # Task is readable => Read + print value
                    str_in = ch_task.read()
                    print("        Current value: %s" % binascii.b2a_hex(ch_task.read()))
                    
                    ############################################################
                    # HERE: Save task value (include perihperal, service, etc) #
                    ############################################################

                else:
                    # Not readable
                    print("        Task '%s' is not readble" %getNameByUUID(ch_task.uuid))

            if (chars is False):
                print("    Service '%s' (with uiid=%s) has no tasks" %(getNameByUUID(se_service.uuid), se_service.uuid))
            print('')
            
        return



#################
### Functions ###
#################

def getNameByUUID(uuid):
    '''Return the name (str) of a uuid. If the uuid is listed in the bluepy Assigned Numbers list or my_ble_names list it will be a human-readable name. Otherwise, it returns the given uuid (str).
    (bluepy Assignment Numbers (str) can be found here: https://ianharvey.github.io/bluepy-doc/assignednumbers.html#assignednumbers)'''
    return my_ble_names.get(str(uuid), UUID(uuid).getCommonName())


def scan_for_ble_devices(scan_time = 10.0, local_device_name = None):
    '''Scan all for all ble devices. It returns a list of all found ble devices.'''
    
    if local_device_name is None:
        return
    
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
