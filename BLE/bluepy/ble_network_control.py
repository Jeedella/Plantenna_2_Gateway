###############################################################
# ble_network_control.py                                      #
# author:   Frank Arts                                        #
# date:     November 6th, 2020                                #
# version:  1.4                                               #
#                                                             #
# version information:                                        #
# - Writing to tasks is now supported.                        #
# - Add method __write_tasks_for_one_periheral()              #
# - Remove method get_addresses()                             #
#                                                             #
# NOTES:                                                      #
# - Mesh networks are not supported                           #
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
spms_ble_names = {
    ## device types ##
    # UUID (key)                            Device type (value)
    "1a310001-63b2-0795-204f-1dda0100d29d": "spms_device",        # 128-bit UUID (not a service, not a task, it is indication)
    
    ## availeble tasks ##
    "1a31fff1-63b2-0795-204f-1dda0100d29d": "availableTasks service", # Not used yet
    "1a31fff2-63b2-0795-204f-1dda0100d29d": "availableTasks task",    # Not used yet
    
    
    ## Services ##
    # UUID (key)                            Service name (value)
    "1a310701-63b2-0795-204f-1dda0100d29d": "Portable Airflow service",
    
    ## Tasks/Characteristics ##
    # UUID (key)                            Task name (value)
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
    This class contains of one or multiple peripherals (= device = node = profile)
    
    ...
    
    attributes
    ----------
    All attributes below are read-only.
    - ID
        Network ID
    
    methods
    -------
    - scanning
    scan_for_new_ble_devices(self, device_type, scan_time = 10.0):
        Scan for new ble devices and asks user to add device to ble network
        device_type must be of type string
        scan_time default value is 10.0 seconds
        
    __scan_for_ble_devices(self, device_type, scan_time = 10.0):
        Scan all for all ble devices. It returns a list containing all found ble devices.
        device_type must be of type string.
        scan_time default value is 10.0 seconds
    
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
    
    
    - task control
    save_tasks(self, peripheral = None, service_uuid = None, task_uuid = None):
        Save one or multiple tasks of one or multiple peripherals
        peripheral must be of type None (all), Peripheral (one) or list (one or multiple)
        service_uuid and task_uuid must be of type None (all), str/unicode (one) or list (one or multiple)
        type of return value depends on the task
        
    __save_tasks_for_one_peripheral(self, peripheral, service_uuid = None, task_uuid = None):
        Save tasks in the memory for one (1) peripheral (currently only printed for debug purposes)
        peripheral must be of type Peripheral
        service_uuid and task_uuid must be of type None (all), str/unicode (one) or list (one or multiple)
        Note: When a service/task is not part of the current peripheral/service, it is ignored

    write_tasks(self, value, peripheral = None, service_uuid = None, task_uuid = None)
        Write 'value' to one or multiple tasks of one or multiple peripherals
        value must be of type str
        peripheral must be of type None (all), Peripheral (one) or list (one or multiple)
        service_uuid and task_uuid must be of type None (all), str/unicode (one) or list (one or multiple)
        
    __write_tasks_for_one_peripheral(self, peripheral, service_uuid = None, task_uuid = None):
        Write 'value' to all, one or multiple tasks of one (1) peripherals (currently with random values for debug purposes)
        value must be of type str
        peripheral must be of type Peripheral
        service_uuid and task_uuid must be of type None (all), str/unicode (one) or list (one or multiple)
    
    ------

    """
    
    # attributes #
    @property
    def netID(self):
        '''Network ID'''
        return self.__netID
    
    
    # consturctor #
    def __init__(self, network_ID, device_type, scan_time = 10.0):
        '''Initialize a dictionary of peripherals and scan for ble device to add to this network
        network_ID should not be of type None. Any other type is acceptable
        device_type must be of type string
        scan_time default value is 10.0 seconds'''
        
        # network ID and empty peripheral dictionary
        self.__netID = network_ID
        self.__peripherals = {}
        
        # Scan for (new) ble devices
        self.scan_for_new_ble_devices(device_type, scan_time)
        
        print('')
        return
    
    # destructor
    def __del__(self):
        '''Delete network with ID x.'''
        print("BLE network '%s' has been deleted." %self.netID)
        return
    
    
    # methods #
    # scanning
    def scan_for_new_ble_devices(self, device_type, scan_time = 10.0):
        '''Scan for new ble devices and asks user to add device to ble network
        device_type must be of type string
        scan_time default value is 10.0 seconds'''
        # Scan for ble devices with name = device_type
        sce_devices = self.__scan_for_ble_devices(device_type, scan_time)
        
        # Check if sce_device is empty (no valid devices found)
        if len(sce_devices) == 0:
            print("No valid devices found (searched for device name: '%s'). Make sure the device is turned on and the correct device_type is searched for." %device_type)
            print('')
            return
        
        # Only add non duplicates to network
        for sce_device in sce_devices:
            # Create Preripheral object from scanEntry object
            p_device = Peripheral(sce_device.addr, sce_device.addrType, sce_device.iface)
            
            # Check duplicate
            if p_device in self.__peripherals:
                # Duplicate
                print("Duplicate is ignored (MAC address=%s)." %p_devcie.addr)
            else:
                # Non duplicate
                response = raw_input("Do you want to connect to device with MAC address %s? [y/N] " % p_device.addr).lower()
                if response == "y" or response == "yes": # Accapted connection
                    print("Connecting to device with MAC address %s" % p_device.addr)
                    self.add_peripherals(p_device)
                else: # Declined connection
                    print("You did not connect to device '%s' with MAC address %s" %(device_type, p_device.addr))
                    continue #skip this device/peripheral
        
        print('')
        return
    
    def __scan_for_ble_devices(self, device_type, scan_time = 10.0):
        '''Scan all for all ble devices. It returns a list containing all found ble devices.
        device_type must be of type string.
        scan_time default value is 10.0 seconds.'''
        
        # Check if device_type is specified
        if device_type is None:
            print("ERROR while trying to scan for ble devices: device_type is not specified. Please try again.")
            return
        
        scanner = Scanner().withDelegate(_ScanDelegate())
        sc_devices = scanner.scan(scan_time)    # Scan for specified time (in seconds) default = 10.0 seconds

        # Create empty list of sce_devices (objects of ScanEntry class)
        sce_devices = []
        
        for device in sc_devices:
            valid_device = False
            print("Device %s (%s), RSSI=%d dB" % (device.addr, device.addrType, device.rssi))
            
            # Display all adtype, desc and value of current device
            for (adtype, desc, value) in device.getScanData(): # adtype (flag), descriptor, value
                if desc == "Complete 128b Services" and getNameByUUID(value) == device_type:
                    print("  %s    %s = %s (uuid=%s)" % (hex(adtype), desc, getNameByUUID(value), value)) # special print
                    
                    valid_device = True;    # Valid device is found (works only for the first device called "Nordic_Blinky"
                    print("Found valid device!")
                    sce_devices.append(device)
                else:
                    print("  %s    %s = %s" % (hex(adtype), desc, value)) # normal print

            # save + print correct device address
            if valid_device:
                print("MAC address valid device: %s\n" %  device.addr)
            else:
                print("Not a valid device!\n")

        return sce_devices
    
    # peripherals
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

    
    # task control
    def save_tasks(self, peripheral = None, service_uuid = None, task_uuid = None):
        '''Save one or multiple tasks of one or multiple peripherals
        peripheral must be of type None (all), Peripheral (one) or list (one or multiple)
        service_uuid and task_uuid must be of type None (all), str/unicode (one) or list (one or multiple)
        type of return value depends on the task'''
                
        # Convert to list
        if peripheral is None:
            peripheral = self.__peripherals.values()
        elif isinstance(peripheral, Peripheral):
            peripheral = [peripheral]
            
        
        # Read
        if (isinstance(peripheral, list)):
            # Remove duplicates
            peripheral = list(dict.fromkeys(peripheral))
            
            for i in range(len(peripheral)):
                addr = self.__peripherals.get(peripheral[i].addr, "not in list")
                if (addr == "not in list"):
                    print("peripheral with MAC address %s is not part of this network (network ID = %s)" %(peripheral[i].addr, self.netID))
                    print("task(s) for this peripheral will not be read")
                else:
                    # read tasks
                    self.__save_tasks_for_one_peripheral(peripheral[i], service_uuid, task_uuid)
        else:
            print("ERROR while trying to save tasks: peripheral is of wrong type (type = %s). Valid type: None, Peripheral or list" %type(peripheral))
        
        print('')
        return
    
    def __save_tasks_for_one_peripheral(self, peripheral, service_uuid = None, task_uuid = None):
        '''Save tasks in the memory for one (1) peripheral (currently only printed for debug purposes)
        peripheral must be of type Peripheral
        service_uuid and task_uuid must be of type None (all), str/unicode (one) or list (one or multiple)
        Note: When a service/task is not part of the current peripheral/service, it is ignored'''
        
        # Convert to list
        if service_uuid == None:
            service_uuid = []
            for service in peripheral.getServices():
                service_uuid.append(service.uuid)
        elif isinstance(service_uuid, str) or isinstance(service_uuid, unicode):
            service_uuid = [service_uuid]
        elif not isinstance(service_uuid, list):
            print("ERROR while trying to save tasks: service_uuid is of wrong type (type = %s). Valid types: None, str, unicode or list" %type(service_uuid))
            return
        
        # Convert to list
        if task_uuid == None:
            task_uuid = []
            for task in peripheral.getCharacteristics():
                task_uuid.append(task.uuid)
        elif isinstance(task_uuid, str):
            task_uuid = [task_uuid]
        elif not isinstance(task_uuid, list):
            print("ERROR while trying to save tasks: task_uuid is of wrong type (type = %s). Valid types: None, str, unicode or list" %type(task_uuid))
            return
        
        if not isinstance(peripheral, Peripheral):
            print("ERROR while trying to save tasks: peripheral is of wrong type (type = %s). Valid type: Peripheral" %type(peripheral))
            return
        
        # Remove duplicates
        service_uuid = list(dict.fromkeys(service_uuid))
        task_uuid    = list(dict.fromkeys(task_uuid))
        
        
        # Print device address
        print("Services and Charactertic uuids of device '%s':" %peripheral.addr)

        
        # Get services
        for se_service in peripheral.getServices():
            if (se_service.uuid not in service_uuid):
                continue    # Skip this sevice
            
            chars = False                # More than 0 tasks?
            firstTask = True             # Fisrt task?
            
            # Save tasks
            for ch_task in se_service.getCharacteristics():
                chars = True
                
                if (ch_task.uuid not in task_uuid):
                    continue;    # Skip this task
                
                if firstTask:
                    # Print current service
                    print("Service:")
                    uuid = se_service.uuid
                    print(getNameByUUID(uuid))
                    print("(uuid=%s)" %uuid)

                    print("    Tasks:")
                    firstTask = False
                
                # Print current task
                uuid = ch_task.uuid
                task_name = getNameByUUID(uuid)
                print("    %s" %task_name)
                print("      (uuid=%s)" %uuid)
                
                
                # Show properties
                print("      %s" %ch_task.propertiesToString())
                        
                # Read task if it supports read
                if(ch_task.supportsRead()):
                    # Task is readable => Read + print value
                    val = ch_task.read()
                    print("        Current value: %s" % binascii.b2a_hex(val))
                    if binascii.b2a_hex(val[-1:]) >= "77": # isReady = 0xFF --> is ready to read
                        # SAVE HERE
                        print("        Saved! (LBS=%s)" % binascii.b2a_hex(val[-1:]))
                    else: # ignore read value, because isRead = 0x00 (< 0x77) --> is not ready to read
                        print("        Ignored! (LBS=%s)" % binascii.b2a_hex(val[-1:]))

                else:
                    # Not readable
                    print("        Task '%s' (uuid=%s) is not readble" %(getNameByUUID(ch_task.uuid), ch_task.uuid))

            if (chars is False):
                print("    Service '%s' (uiid=%s) has no tasks" %(getNameByUUID(se_service.uuid), se_service.uuid))
            print('')
            
        return
    
    def write_tasks(self, value, peripheral = None, service_uuid = None, task_uuid = None):
        '''Write 'value' to one or multiple tasks of one or multiple peripherals
        value must be of type str
        peripheral must be of type None (all), Peripheral (one) or list (one or multiple)
        service_uuid and task_uuid must be of type None (all), str/unicode (one) or list (one or multiple)'''
        
        # Check type of value
        if not isinstance(value, str):
            print("ERROR while trying to write tasks: value (%s) is of wrong type (type = %s). Valid type: int or str" %(value, type(value)))
            print('')
            return
        
        # Convert to list
        if peripheral is None:
            peripheral = self.__peripherals.values()
        elif isinstance(peripheral, Peripheral):
            peripheral = [peripheral]
            
        
        # Write
        if (isinstance(peripheral, list)):
            # Remove duplicates
            peripheral = list(dict.fromkeys(peripheral))
            
            for i in range(len(peripheral)):
                addr = self.__peripherals.get(peripheral[i].addr, "not in list")
                if (addr == "not in list"):
                    print("peripheral with MAC address %s is not part of this network (network ID = %s)" %(peripheral[i].addr, self.netID))
                    print("task(s) for this peripheral will not be written")
                else:
                    # write tasks
                    self.__write_tasks_for_one_peripheral(value, peripheral[i], service_uuid, task_uuid)
        else:
            print("ERROR while trying to write tasks: peripheral is of wrong type (type = %s). Valid type: None, Peripheral or list" %type(peripheral))
        
        print('')
        return
    
    def __write_tasks_for_one_peripheral(self, value, peripheral, service_uuid = None, task_uuid = None):
        '''Write 'value' to all, one or multiple tasks of one (1) peripherals (currently with random values for debug purposes)
        value must be of type str
        peripheral must be of type Peripheral
        service_uuid and task_uuid must be of type None (all), str/unicode (one) or list (one or multiple)'''
        
        # Convert to list
        if service_uuid == None:
            service_uuid = []
            for service in peripheral.getServices():
                service_uuid.append(service.uuid)
        elif isinstance(service_uuid, str) or isinstance(service_uuid, unicode):
            service_uuid = [service_uuid]
        elif not isinstance(service_uuid, list):
            print("ERROR while trying to save tasks: service_uuid is of wrong type (type = %s). Valid types: None, str, unicode or list" %type(service_uuid))
            return
        
        # Convert to list
        if task_uuid == None:
            task_uuid = []
            for task in peripheral.getCharacteristics():
                task_uuid.append(task.uuid)
        elif isinstance(task_uuid, str):
            task_uuid = [task_uuid]
        elif not isinstance(task_uuid, list):
            print("ERROR while trying to save tasks: task_uuid is of wrong type (type = %s). Valid types: None, str, unicode or list" %type(task_uuid))
            return
        
        if not isinstance(peripheral, Peripheral):
            print("ERROR while trying to save tasks: peripheral is of wrong type (type = %s). Valid type: Peripheral" %type(peripheral))
            return
        
        # Remove duplicates
        service_uuid = list(dict.fromkeys(service_uuid))
        task_uuid    = list(dict.fromkeys(task_uuid))
        
        
        # Print device address
        print("Services and Charactertic uuids of device '%s':" %peripheral.addr)

        
        # Get services
        for se_service in peripheral.getServices():
            if (se_service.uuid not in service_uuid):
                continue    # Skip this sevice
            
            chars = False                # More than 0 tasks?
            firstTask = True             # Fisrt task?
            
            # Save tasks
            for ch_task in se_service.getCharacteristics():
                chars = True
                
                if (ch_task.uuid not in task_uuid):
                    continue;    # Skip this task
                
                if firstTask:
                    # Print current service
                    print("Service:")
                    uuid = se_service.uuid
                    print(getNameByUUID(uuid))
                    print("(uuid=%s)" %uuid)

                    print("    Tasks:")
                    firstTask = False
                
                # Print current task
                uuid = ch_task.uuid
                task_name = getNameByUUID(uuid)
                print("    %s" %task_name)
                print("      (uuid=%s)" %uuid)
                
                
                # Show properties
                print("      %s" %ch_task.propertiesToString())
                        
                # Write task if it supports writing
                if (ch_task.properties & ch_task.props["WRITE"]):
                    # Task is readable => Write + print written value
                    ch_task.write(value)
                    print("        Written value: %s" %repr(value))
                else:
                    # Not readable
                    print("        Task '%s' (uuid=%s) is not writable" %(getNameByUUID(ch_task.uuid), ch_task.uuid))

            if (chars is False):
                print("    Service '%s' (uiid=%s) has no tasks" %(getNameByUUID(se_service.uuid), se_service.uuid))
            print('')
            
        return



########################
### Global functions ###
########################

def getNameByUUID(uuid):
    '''Return the name (str) of a uuid. If the uuid is listed in the bluepy Assigned Numbers list or spms_ble_names list it will be a human-readable name. Otherwise, it returns the given uuid (str).
    (bluepy Assignment Numbers (str) can be found here: https://ianharvey.github.io/bluepy-doc/assignednumbers.html#assignednumbers)'''
    return spms_ble_names.get(str(uuid), UUID(uuid).getCommonName())
