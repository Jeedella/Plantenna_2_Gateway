###############################################################
# ble_network_control.py                                      #
# author:   Frank Arts                                        #
# date:     December 31st, 2020                               #
# version:  1.9                                               #
#                                                             #
# version info:                                               #
# - Data is no longer converted in handleDiscovery            #
# - Convert endian of ble data to little-endian               #
#                                                             #
# NOTES:                                                      #
# - Mesh networks are not supported                           #
###############################################################

# import

import local_database
from bluepy.btle import Scanner, DefaultDelegate, Service
from bluepy.btle import UUID, Peripheral, AssignedNumbers
from bluepy.btle import ADDR_TYPE_PUBLIC, ADDR_TYPE_RANDOM
import spms_cloud_control
from spms_cloud_control import spms_mqtt_init, spms_mqtt_send_data, spms_mqtt_stop
import sys, binascii

###################
## my dictionary ##
###################

# my dictionary of uuids (services and characteristics)
myAir_ble_names = {
    ## broadast uuids/device type ##
    # UUID (key)                            Profile (value)
    "1a310101-63b2-0795-204f-1dda0100d29d": "Portable Profile Finedust broadcast",
    
    "1a310201-63b2-0795-204f-1dda0100d29d": "Portable Profile CO2 broadcast",
    
    "1a310301-63b2-0795-204f-1dda0100d29d": "Portable Profile NH3 broadcast",
    
    "1a310401-63b2-0795-204f-1dda0100d29d": "Fixed Profile Finedust broadcast",
    
    "1a310501-63b2-0795-204f-1dda0100d29d": "Fixed Profile CO2 broadcast",
    
    "1a310601-63b2-0795-204f-1dda0100d29d": "Fixed Profile NH3 broadcast",
    
    # Tasks: Services and characteristics
    # UUID (key)                            Service/characteristic name (value) 
    "1a310102-63b2-0795-204f-1dda0100d29d": "Portable Profile Finedust service",
    "1a310103-63b2-0795-204f-1dda0100d29d": "Portable Profile Finedust characteristic",
    
    "1a310202-63b2-0795-204f-1dda0100d29d": "Portable Profile CO2 service",
    "1a310203-63b2-0795-204f-1dda0100d29d": "Portable Profile CO2 characteristic",
    
    "1a310302-63b2-0795-204f-1dda0100d29d": "Portable Profile NH3 service",
    "1a310303-63b2-0795-204f-1dda0100d29d": "Portable Profile NH3 characteristic",
    
    "1a310402-63b2-0795-204f-1dda0100d29d": "Fixed Profile Finedust service",
    "1a310403-63b2-0795-204f-1dda0100d29d": "Fixed Profile Finedust characteristic",
    
    "1a310502-63b2-0795-204f-1dda0100d29d": "Fixed Profile CO2 service",
    "1a310503-63b2-0795-204f-1dda0100d29d": "Fixed Profile CO2 characteristic",
    
    "1a310602-63b2-0795-204f-1dda0100d29d": "Fixed Profile NH3 service",
    "1a310603-63b2-0795-204f-1dda0100d29d": "Fixed Profile NH3 characteristic",
}

spms_ble_names = {
    ## broadast uuids/device type ##
    # UUID (key)                            Profile (value)
    "1a310701-63b2-0795-204f-1dda0100d29d": "spms_device",
    
    ## availeble tasks --> all data that was gathered while connection was lost ##
    "1a31fff1-63b2-0795-204f-1dda0100d29d": "availableTasks service",        # Not used yet
    "1a31fff2-63b2-0795-204f-1dda0100d29d": "availableTasks characteristic", # Not used yet
    
    # Services and characteristics
    # UUID (key)                            Service/characteristic name (value)
    "1a310702-63b2-0795-204f-1dda0100d29d": "Portable Airflow service",
    "1a310703-63b2-0795-204f-1dda0100d29d": "Portable Airflow characteristic",
}


###############
### Classes ###
###############

# DeviceScanDelegate class
class _DeviceScanDelegate(DefaultDelegate):
    '''
    DeviceScanDelegate class, subclass of DefaultDelegate class, provides the handleDiscovery method.
    
    ...
    
    methods
    -------
    handleDiscovery(self, dev, isNewDev, isNewData)
        Handle discovery for the scanEntry class
    
    '''
    
    def __init__(self):
        '''Initialize the _ScanDelecate class: use init of DefualtDelegate'''
        DefaultDelegate.__init__(self)
        return

    def handleDiscovery(self, dev, isNewDev, isNewData):
        '''Handle discovery for new devices and data in the scanEntry class'''
        if isNewDev:
            print("Discovered device %s" % dev.addr)
        elif isNewData:
            print("Received new data from %s" % dev.addr)
        return


# DataScanDelegate class
class _DataScanDelegate(DefaultDelegate):
    '''
    DataScanDelegate class, subclass of DefaultDelegate class, provides the handleDiscovery method.
    
    ...
    
    methods
    -------
    handleDiscovery(self, dev, isNewDev, isNewData)
        Handle discovery for the scanEntry class
    
    '''
    
    def __init__(self):
        '''Initialize the _ScanDelecate class: use init of DefualtDelegate'''
        DefaultDelegate.__init__(self)
        return

    def handleDiscovery(self, dev, isNewDev, isNewData):
        '''Handle discovery of new data in the scanEntry class'''
        if isNewData:
            data = None
            for adtype, desc, val in dev.getScanData():
                # Read dat if correct decripion
                if desc == "Manufacturer":
                    data = val
                
                # Print data if correct device/profile AND data was received
                if val in myAir_ble_names.keys() and data is not None:
                    # Print data
                    print("Received new data from %s:" % dev.addr)
                    print_ble_data(data, "myAir", "LITTLE_ENDIAN")
                    print('')
            
            # Save data
            ### UPDATE me ###
            
        return


# NotifyDelegate class
class _NotifyDelegate(DefaultDelegate):
    '''
    ScanDelegate class, subclass of DefaultDelegate class, provides the handleNotifictions method.
    
    ...
    
    methods
    -------
    handleNotifications(self, cHandle, data)
        Handle notifications for the Peripheral class
    
    '''
    
    def __init__(self):
        '''Initialize the _ScanDelecate class: use init of DefualtDelegate'''
        DefaultDelegate.__init__(self)
        self.__spms_mqtt_client = spms_mqtt_init()
        return

    def handleNotification(self, cHandle, data):
        '''Handle notifications for the Peripherals class'''
        print("Received notification from handle %s" % cHandle)
        
        data_hex = binascii.b2a_hex(data)
        print("Current value: %s" % data_hex)    
        
#         save_ble_data(data_hex, LITTLE_ENDIAN)
        
#         print_spms_data(data_hex)
#         
#         temp     = float.fromhex(data_hex[8:12])/100
#         humid    = float.fromhex(data_hex[12:16])/100
#         pressure = float.fromhex(data_hex[16:20])
#         
#         print(temp, humid, pressure)
#         spms_mqtt_send_data(self.__spms_mqtt_client, temp, humid, pressure)
        
        print("")
        return



# BLE network class
class BLE_network:
    """
    BLE network class
    < UNDER DEVELOPMENT >
    This class contains of one or multiple peripherals (= device = node = profile). Each of these peripherals can be read from and written to. In addition, if the characteristic supports NOTIFY (notifications), these can also be read.
    
    ...
    
    attributes
    ----------
    All attributes below are read-only.
    - netID
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
    add_peripherals(self, peripheral_addr, addrType = ADDR_TYPE_PUBLIC, iface = None)
        Add one or mutliple peripherals
        peripheral_addr must be of type str/unicode (one) or list (one or multiple)
        addrType and iface must be the same for all peripherals
    
    delete_peripherals(self, peripheral_addr = None)
        Delete all peripherals or specified peripheral(s) with MAC address peripheral_addr
        peripheral_addr must be of type None (all) str/unicode (one) or list (one or multiple)
   
    get_peripherals(self, peripheral_addr = None)
        Return a list containing the Peripherals of all peripherals or specified peripheral(s)
        peripheral_addr must be of type None (all), str/unicode (one) or list (one or multiple)
    
    
    - Characteristic control
    read_characteristics(self, peripheral = None, service_uuid = None, characteristic_uuid = None)
        Read and save one or multiple characteristics of one or multiple peripherals
        peripheral must be of type None (all), Peripheral (one) or list (one or multiple)
        service_uuid and characteristic_uuid must be of type None (all), str/unicode (one) or list (one or multiple)
        type of return value depends on the characteristic
        
    __read_characteristics_for_one_peripheral(self, peripheral, service_uuid = None, characteristic_uuid = None)
        Read and save characteristics in the memory for one (1) peripheral (currently only printed for debug purposes)
        peripheral must be of type Peripheral
        service_uuid and characteristic_uuid must be of type None (all), str/unicode (one) or list (one or multiple)
        Note: When a service/characteristic is not part of the current peripheral/service, it is ignored

    write_characteristics(self, value, peripheral = None, service_uuid = None, characteristic_uuid = None)
        Write 'value' to one or multiple characteristics of one or multiple peripherals
        value must be of type str
        peripheral must be of type None (all), Peripheral (one) or list (one or multiple)
        service_uuid and characteristic_uuid must be of type None (all), str/unicode (one) or list (one or multiple)
        
    __write_characteristics_for_one_peripheral(self, peripheral, service_uuid = None, characteristic_uuid = None):
        Write 'value' to all, one or multiple characteristics of one (1) peripherals (currently with random values for debug purposes)
        value must be of type str
        peripheral must be of type Peripheral
        service_uuid and characteristic_uuid must be of type None (all), str/unicode (one) or list (one or multiple)
    
    - Delegates
    enable_notifications(self, peripheral = None, characteristic_uuid = None, timeout = 2.0, enable = True)
        Enable/Disable notifications for the specified characteristic(s) on the specified peripheral(s)
        peripheral must be of type None (all), Peripheral (one) or list (one or multiple)
        characteristic must be of type None (all) or str (one)
        timeout has a default value of 2.0 seconds
        To disable, set enable = False
        
    enable_broadcast_data_receive(self, enable = True)
        Enable/Disable receiving of broadcast data
        To disable, set enable = False
    
    receive_broadcast_data(self, timeout = 10)
        If new data is availabe, receive broadcast data (must be enabled before)
        stops when timeout is reached and may be called multiple times when broadcast data is enabled
        this method must be called continuously if broadcastdata can't be missed
        NOTE: _DataScanDelegete.handleDiscovery() is called when data is received
    
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
        
        
        # my mqtt init
        self.__spms_mqtt_client = spms_mqtt_init()
        
        # Reset broadcastDataReceiveEnabled
        self.__broadcastDataReceiveEnabled = False
        
        
        print('')
        return
    
    # destructor
    def __del__(self):
        '''Delete network with ID x.'''
        print('')
        
        # Disconnnect from alll peripherals
        for addr, p in self.__peripherals.iteritems():
            print("Disconencting from device with MAC address %s ..." %addr)
            p.disconnect()
            print("Disconnecting successfull")
        
        # Terminate connection to cloud
        spms_mqtt_stop(self.__spms_mqtt_client)
        print("Connection with cloud has been terminated.")
        
        # BLE network has been deleted
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
            print("No valid devices found (searched for device type: '%s' (uuid=%s)). Make sure the device is turned on and the correct device_type is searched for." %(device_type, getNameByUUID(device_type)))
            print('')
            return
        
        # Only add non duplicates to network
        for sce_device in sce_devices:
            # Check duplicate
            if sce_device.addr in self.__peripherals.keys():
                # Duplicate
                print("Duplicate is ignored (MAC address=%s)." %sce_device.addr)
            else:
                # Non duplicate
                response = raw_input("Do you want to connect to device with MAC address %s? [y/N] " % sce_device.addr).lower()
                if response == "y" or response == "yes": # Accepted connection
                    print("Connecting to device with MAC address %s" % sce_device.addr)
                    self.add_peripherals(sce_device.addr, sce_device.addrType, sce_device.iface)
                else: # Declined connection
                    print("You did not connect to device '%s' with MAC address %s" %(device_type, sce_device.addr))
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
        
        scanner = Scanner().withDelegate(_DeviceScanDelegate())
        sc_devices = scanner.scan(scan_time)    # Scan for specified time (in seconds) default = 10.0 seconds

        # Create empty list of sce_devices (objects of ScanEntry class)
        sce_devices = []
        
        for device in sc_devices:
            valid_device = False
            print("Device %s (%s), RSSI=%d dB" % (device.addr, device.addrType, device.rssi))
            
            # Display all adtype, desc and value of current device
            for (adtype, desc, value) in device.getScanData(): # adtype (flag), descriptor, value
                if desc == "Complete Local Name" and value == device_type:
                    print("  %s    %s = %s" % (hex(adtype), desc, value)) # normal print
#                 if desc == "Complete 128b Services" and getNameByUUID(value) == device_type:
#                     print("  %s    %s = %s (uuid=%s)" % (hex(adtype), desc, getNameByUUID(value), value)) # special print
                    
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
    def add_peripherals(self, peripheral_addr, addrType = ADDR_TYPE_PUBLIC, iface = None):
        '''Add one or mutliple peripherals
        peripheral_addr must be of type str/unicode (one) or list (one or multiple)
        addrType and iface must be the same for all peripherals'''
        
        # Convert to list
        if (isinstance(peripheral_addr, str) or isinstance(peripheral_addr, unicode)):
            peripheral_addr = [peripheral_addr]
            
            
        # Add
        if (isinstance(peripheral_addr, list)):
            # Remove duplicates
            peripheral_addr = list(dict.fromkeys(peripheral_addr))
            
            print("Added peripherals to network with network ID: '%s'" %self.netID)
            for i in range(len(peripheral_addr)):
                no_repeat = False
                no_repeat = self.__peripherals.get(peripheral_addr[i], True)
                
                # Create Preripheral object from scanEntry object + Connect to it
                p_device = Peripheral(peripheral_addr[i], addrType, iface)
                self.__peripherals[peripheral_addr[i]] = p_device
                
                if (no_repeat == True):
                    print("    [new] Added peripheral has MAC address: %s" %peripheral_addr[i])
                else:
                    print("    [update] Updated peripheral has MAC address: %s" %peripheral_addr[i])
        else:
            print("ERROR while trying to add peripherals: peripheral is of wrong type (type = %s). Valid types: Peripheral, list (of Peripheral)" %type(peripheral))
        
        print('')
        return
    
    def delete_peripherals(self, peripheral_addr = None):
        '''Delete all peripherals or specified peripheral(s) with MAC address peripheral_addr
        peripheral_addr must be of type None (all) str/unicode (one) or list (one or multiple)'''
        
        # Convert to list
        if (isinstance(peripheral_addr, str) or isinstance(peripheral_addr, unicode)):
            peripheral_addr = [peripheral_addr]
            
            
        # Delete
        if (peripheral_addr == None):
            # Disable notifications
            self.enable_notifications(enable = False)
            
            for addr, p in self.__peripherals.iteritems():
                print("Disconencting from device with MAC address %s ..." %addr)
                p.disconnect()
                print("Successfully disconnected")
            
            self.__peripherals.clear()
            print("Deleted all peripherals from this network")
        elif (isinstance(peripheral_addr, list)):
            # Remove duplicates
            peripheral_addr = list(dict.fromkeys(peripheral_addr))
            
            for i in range(len(peripheral_addr)):
                p = self.__peripherals.get(peripheral_addr[i], "Not in list")
                if p != "Not in list":
                    # Disable notifications
                    self.enable_notifications(peripheral = p, enable = False)
                    
                    # Disconnect
                    print("Disconencting from device with MAC address %s ..." %peripheral_addr[i])
                    self.__peripherals[peripheral_addr[i]].disconnect()
                    print("Disonnecting successfull")
                    
                    # Delete
                    self.__peripherals.pop(peripheral_addr[i])
                    print("Deleted peripheral with MAC address %s from network" %peripheral_addr[i])
                else:
                    print("peripheral with MAC address %s is not part of this network (network ID = %s)" %(peripheral_addr[i], self.netID))
        else:
            print("ERROR while trying to delete peripherals: peripheral is of wrong type (type = %s). Valid types: None, unicode, str or list (of unicode/str)" %type(peripheral_addr))
        
        print('')
        return
    
    def get_peripherals(self, peripheral_addr = None):
        '''Return a list containing the Peripherals of all peripherals or specified peripheral(s)
        peripheral_addr must be of type None (all), str/unicode (one) or list (one or multiple)'''
        p = []
                
        # Convert to list
        if (isinstance(peripheral_addr, str) or isinstance(peripheral_addr, unicode)):
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

    
    # Characteristic control
    def read_characteristics(self, peripheral = None, service_uuid = None, characteristic_uuid = None):
        '''Read and save one or multiple characteristics of one or multiple peripherals
        peripheral must be of type None (all), Peripheral (one) or list (one or multiple)
        service_uuid and characteristic_uuid must be of type None (all), str/unicode (one) or list (one or multiple)
        type of return value depends on the characteristic'''
                
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
                    print("characteristic(s) for this peripheral will not be read")
                else:
                    # read characteristics
                    self.__read_characteristics_for_one_peripheral(peripheral[i], service_uuid, characteristic_uuid)
        else:
            print("ERROR while trying to save characteristics: peripheral is of wrong type (type = %s). Valid type: None, Peripheral or list" %type(peripheral))
        
        print('')
        return
    
    def __read_characteristics_for_one_peripheral(self, peripheral, service_uuid = None, characteristic_uuid = None):
        '''Read and save characteristics in the memory for one (1) peripheral (currently only printed for debug purposes)
        peripheral must be of type Peripheral
        service_uuid and characteristic_uuid must be of type None (all), str/unicode (one) or list (one or multiple)
        Note: When a service/characteristic is not part of the current peripheral/service, it is ignored'''
        
        # Convert to list
        if service_uuid is None:
            service_uuid = []
            for service in peripheral.getServices():
                service_uuid.append(service.uuid)
        elif isinstance(service_uuid, str) or isinstance(service_uuid, unicode):
            service_uuid = [service_uuid]
        elif not isinstance(service_uuid, list):
            print("ERROR while trying to save characteristics: service_uuid is of wrong type (type = %s). Valid types: None, str, unicode or list" %type(service_uuid))
            return
        
        # Convert to list
        if characteristic_uuid is None:
            characteristic_uuid = []
            for characteristic in peripheral.getCharacteristics():
                characteristic_uuid.append(characteristic.uuid)
        elif isinstance(characteristic_uuid, str) or isinstance(characteristic_uuid, unicode):
            characteristic_uuid = [characteristic_uuid]
        elif not isinstance(characteristic_uuid, list):
            print("ERROR while trying to save characteristics: characteristic_uuid is of wrong type (type = %s). Valid types: None, str, unicode or list" %type(characteristic_uuid))
            return
        
        if not isinstance(peripheral, Peripheral):
            print("ERROR while trying to save characteristics: peripheral is of wrong type (type = %s). Valid type: Peripheral" %type(peripheral))
            return
        
        # Remove duplicates
        service_uuid = list(dict.fromkeys(service_uuid))
        characteristic_uuid    = list(dict.fromkeys(characteristic_uuid))
        
        
        # Print device address
        print("Services and Charactertic uuids of device '%s':" %peripheral.addr)

        
        # Get services
        for se_service in peripheral.getServices():
            if (se_service.uuid not in service_uuid):
                continue    # Skip this sevice
            
            chars = False                # More than 0 characteristics?
            firstCharacteristic = True             # Fisrt characteristic?
            
            # Save characteristics
            for ch_characteristic in se_service.getCharacteristics():
                chars = True
                
                if (ch_characteristic.uuid not in characteristic_uuid):
                    continue;    # Skip this characteristic
                
                if firstCharacteristic:
                    # Print current service
                    print("Service:")
                    uuid = se_service.uuid
                    print(getNameByUUID(uuid))
                    print("(uuid=%s)" %uuid)

                    print("    Characteristics:")
                    firstCharacteristic = False
                
                # Print current characteristic
                uuid = ch_characteristic.uuid
                characteristic_name = getNameByUUID(uuid)
                print("    %s" %characteristic_name)
                print("      (uuid=%s)" %uuid)
                
                
                # Show properties
                print("      %s" %ch_characteristic.propertiesToString())
                        
                # Read characteristic if it supports read
                if (ch_characteristic.supportsRead() and characteristic_name != "Battery Level"):
                    # Characteristic is readable => Read + print value
                    val = ch_characteristic.read()
                    data = binascii.b2a_hex(val)
                    print("        Current value: %s" % data)
                    if data[-1:] >= "77": # isReady == 0xFF --> is ready to read
                        # Send data to cloud
                        print("        Value: %s" % data)
                        
                        # Only send to cloud when its spms data
                        inDict = spms_ble_names.get(str(uuid), "Not in dict")
                        
                        if inDict is not "Not in dict":
                            print_ble_data(data, "spms", "LITTLE_ENDIAN")

##                            send_data_to_database(data)
##                            temperature = int(data[8:12], 16)
##                            humidity = int(data[12:16], 16)
##                            batV = int(data[20:22], 16)
##                            pressure = int(data[16:20])
##                            status = int(data[22:24])
##                            airflow = int(data[24:28])
##                            print(temperature, humidity, batV, pressure, airflow)
##                            local_database.insert_data(temperature, humidity, batV, airflow, pressure)
##                            spms_mqtt_send_data(self.__spms_mqtt_client, temp, humid, pressure, batV, airflow)
                            
                            #save_data(peripheral.addr, val)
                        
                        # Print that data is saved
                        print("        Saved! (LBS=%s)" % binascii.b2a_hex(data[-1:]))
                    else: # ignore read value, because isRead = 0x00 (< 0x77) --> is not ready to read
                        print("        Ignored! (LBS=%s)" % binascii.b2a_hex(data[-1:]))

                else:
                    # Not readable
                    print("        Characteristic '%s' (uuid=%s) is not readble" %(getNameByUUID(ch_characteristic.uuid), ch_characteristic.uuid))

            if (chars is False):
                print("    Service '%s' (uiid=%s) has no characteristics" %(getNameByUUID(se_service.uuid), se_service.uuid))
            print('')
            
        return
    
    def write_characteristics(self, value, peripheral = None, service_uuid = None, characteristic_uuid = None):
        '''Write 'value' to one or multiple characteristics of one or multiple peripherals
        value must be of type str
        peripheral must be of type None (all), Peripheral (one) or list (one or multiple)
        service_uuid and characteristic_uuid must be of type None (all), str/unicode (one) or list (one or multiple)'''
        
        # Check type of value
        if not isinstance(value, str):
            print("ERROR while trying to write characteristics: value (%s) is of wrong type (type = %s). Valid type: int or str" %(value, type(value)))
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
                    print("characteristic(s) for this peripheral will not be written")
                else:
                    # write characteristics
                    self.__write_characteristics_for_one_peripheral(value, peripheral[i], service_uuid, characteristic_uuid)
        else:
            print("ERROR while trying to write characteristics: peripheral is of wrong type (type = %s). Valid type: None, Peripheral or list" %type(peripheral))
        
        print('')
        return
    
    def __write_characteristics_for_one_peripheral(self, value, peripheral, service_uuid = None, characteristic_uuid = None):
        '''Write 'value' to all, one or multiple characteristics of one (1) peripherals (currently with random values for debug purposes)
        value must be of type str
        peripheral must be of type Peripheral
        service_uuid and characteristic_uuid must be of type None (all), str/unicode (one) or list (one or multiple)'''
        
        # Convert to list
        if service_uuid is None:
            service_uuid = []
            for service in peripheral.getServices():
                service_uuid.append(service.uuid)
        elif isinstance(service_uuid, str) or isinstance(service_uuid, unicode):
            service_uuid = [service_uuid]
        elif not isinstance(service_uuid, list):
            print("ERROR while trying to write characteristics: service_uuid is of wrong type (type = %s). Valid types: None, str, unicode or list" %type(service_uuid))
            return
        
        # Convert to list
        if characteristic_uuid is None:
            characteristic_uuid = []
            for characteristic in peripheral.getCharacteristics():
                characteristic_uuid.append(characteristic.uuid)
        elif isinstance(characteristic_uuid, str) or isinstance(characteristic_uuid, unicode):
            characteristic_uuid = [characteristic_uuid]
        elif not isinstance(characteristic_uuid, list):
            print("ERROR while trying to save characteristics: characteristic_uuid is of wrong type (type = %s). Valid types: None, str, unicode or list" %type(characteristic_uuid))
            return
        
        if not isinstance(peripheral, Peripheral):
            print("ERROR while trying to save characteristics: peripheral is of wrong type (type = %s). Valid type: Peripheral" %type(peripheral))
            return
        
        # Remove duplicates
        service_uuid = list(dict.fromkeys(service_uuid))
        characteristic_uuid    = list(dict.fromkeys(characteristic_uuid))
        
        
        # Print device address
        print("Services and Charactertic uuids of device '%s':" %peripheral.addr)

        
        # Get services
        for se_service in peripheral.getServices():
            if (se_service.uuid not in service_uuid):
                continue    # Skip this sevice
            
            chars = False                # More than 0 characteristics?
            firstCharacteristic = True             # Fisrt characteristic?
            
            # Save characteristics
            for ch_characteristic in se_service.getCharacteristics():
                chars = True
                
                if (ch_characteristic.uuid not in characteristic_uuid):
                    continue;    # Skip this characteristic
                
                if firstCharacteristic:
                    # Print current service
                    print("Service:")
                    uuid = se_service.uuid
                    print(getNameByUUID(uuid))
                    print("(uuid=%s)" %uuid)

                    print("    Characteristics:")
                    firstCharacteristic = False
                
                # Print current characteristic
                uuid = ch_characteristic.uuid
                characteristic_name = getNameByUUID(uuid)
                print("    %s" %characteristic_name)
                print("      (uuid=%s)" %uuid)
                
                
                # Show properties
                print("      %s" %ch_characteristic.propertiesToString())
                        
                # Write characteristic if it supports writing
                if (ch_characteristic.properties & ch_characteristic.props["WRITE"]):
                    # Characteristic is readable => Write + print written value
                    ch_characteristic.write(value)
                    print("        Written value: %s" %repr(value))
                else:
                    # Not readable
                    print("        Characteristic '%s' (uuid=%s) is not writable" %(getNameByUUID(ch_characteristic.uuid), ch_characteristic.uuid))
        
        return
    
    # Delegate
    def enable_notifications(self, peripheral = None, characteristic_uuid = None, timeout = 2.0, enable = True):
        '''Enable/Disable notifications for the specified characteristic(s) on the specified peripheral(s)
        peripheral must be of type None (all), Peripheral (one) or list (one or multiple)
        characteristic must be of type None (all) or str (one)
        timeout has a default value of 2.0 seconds
        To disable, set enable = False'''
            
        # Convert to peripheral list
        if peripheral is None:
            peripheral = self.__peripherals.values()
        elif isinstance(peripheral, Peripheral):
            peripheral = [peripheral]
            
        
        # Handle notifications
        if (isinstance(peripheral, list)):
            # Remove duplicates
            peripheral = list(dict.fromkeys(peripheral))
            
            for i in range(len(peripheral)):
                addr = self.__peripherals.get(peripheral[i].addr, "not in list")
                if (addr == "not in list"):
                    print("peripheral with MAC address %s is not part of this network (network ID = %s)" %(peripheral[i].addr, self.netID))
                    print("Notifications for this peripheral will not be enabled")
                else:
                    # Convert to characteristic list
                    if (characteristic_uuid is None or isinstance(characteristic_uuid, str)):
                        ch_characteristics = peripheral[i].getCharacteristics(uuid = characteristic_uuid)
                        for j in range(len(ch_characteristics)):
                           if (ch_characteristics[j].properties & ch_characteristics[j].props["NOTIFY"] and ch_characteristics[j].uuid != "00002a19-0000-1000-8000-00805f9b34fb"):
                                handle = ch_characteristics[j].getHandle()
                                currently_disabled = peripheral[i].readCharacteristic(handle + 1)
                                currently_disabled = binascii.b2a_hex(currently_disabled)
                                
                                if enable:
                                    if currently_disabled:
                                        # with _NotifyDelegate
                                        peripheral[i].withDelegate(_NotifyDelegate())
                        
                                        # Enable notifications
                                        peripheral[i].writeCharacteristic(handle + 1, b"\x01\x00", True)
                                        print("Notifications enabled for characteristic %s on peripheral %s" %(ch_characteristics[j].uuid, peripheral[i].addr))
                                    else:
                                        print("Notifications are already enabled for characteristic %s on peripheral %s" %(ch_characteristics[j].uuid, peripheral[i].addr))
                                else:
                                    if currently_disabled:
                                        # Disable notifications
                                        peripheral[i].writeCharacteristic(handle + 1, b"\x00\x00", True)
                                        print("Notifications disabled for characteristic %s on peripheral %s" %(ch_characteristics[j].uuid, peripheral[i].addr))
                                    else:
                                        print("Notifications are already disabled for characteristic %s on peripheral %s" %(ch_characteristics[j].uuid, peripheral[i].addr))
                    else:
                        print("ERROR while trying to enable notifications: characteristic_uuid is of wrong type (type = %s). Valid type: None or str" %type(characteristic_uuid))
        else:
            print("ERROR while trying to enable notifications: peripheral is of wrong type (type = %s). Valid type: None, Peripheral or list" %type(peripheral))
        
        print('')
        return
        
        
    def enable_broadcast_data_receive(self, enable = True):
        '''Enable/Disable receiving of broadcast data
        To disable, set enable = False'''
        
        # Enable/Disable
        if enable == True and self.__broadcastDataReceiveEnabled == False:
            self.broadcastDataReceiveScanner = Scanner().withDelegate(_DataScanDelegate())
            self.broadcastDataReceiveScanner.start()
            self.__broadcastDataReceiveEnabled = True
            print("Broadcast data receive is enabled.")
        elif enable == False and self.__broadcastDataReceiveEnabled == True:
            self.broadcastDataReceiveScanner.stop()
            self.__broadcastDataReceiveEnabled = False
            print("Broadcast data receive is disabled.")
                    
        print('')
        return
    
    def receive_broadcast_data(self, timeout = 10):
        '''If new data is availabe, receive broadcast data (must be enabled before)
        stops when timeout is reached and may be called multiple times when broadcast data is enabled
        this method must be called continuously if broadcastdata can't be missed
        NOTE: _DataScanDelegete.handleDiscovery() is called when data is received'''
        
        if self.__broadcastDataReceiveEnabled == True:
            self.broadcastDataReceiveScanner.process(timeout = timeout)
            print('')
            print("Checking for new broadcast data...")
        else:
            print("ERROR: Braodcast receive is not enabled. Enabled with: BLE_network.enable_broadcast_data_receive(enable = True).")
            print('')
        
        return


########################
### Global functions ###
########################

def getNameByUUID(uuid):
    '''Return the name (str) of a uuid. If the uuid is listed in the bluepy Assigned Numbers list or spms_ble_names list or myAir_ble_names list, it will be a human-readable name. Otherwise, it returns the given uuid (str).
    (bluepy Assignment Numbers (str) can be found here: https://ianharvey.github.io/bluepy-doc/assignednumbers.html#assignednumbers)'''
    name = spms_ble_names.get(str(uuid), uuid)
    
    if name is uuid:
        name = myAir_ble_names.get(str(uuid), uuid)
    
    try:
        if name is uuid:
            name = UUID(uuid).getCommonName() # NOTE: Raises TypeError when name is given
    except TypeError:
        return uuid
        
    return name


def save_ble_data(data, endian = "LITTLE_ENDIAN"):
    '''Save ble data in database
    endian can be either LITTLE_ENDIAN or BIG_ENDIAN'''
    endian = endian.upper()
    
    # Check endian
    if endian == "LITTLE_ENDIAN":
        # Convert unicode to list (via string)
        data = list(str(data))
        print(data)
        
        # Convert to big endian
        for i in range(0, len(data), 4):
            tmp           = data[i:i+2]
            data[i:i+2]   = data[i+2:i+4]
            data[i+2:i+4] = tmp
        
        endian = "BIG_ENDIAN"
        
        # Convert back to string
        data = ''.join(data)
    
    if endian == "BIG_ENDIAN":
        # Save data in database
        ## UPDATE ME ##
        pass
        
    else:
        print("Endian is not correct. Allowed endians: LITTLE_ENDIAN or BIG_ENDIAN" %endian)
    

def print_ble_data(data, devType = "SPMS", endian = "LITTLE_ENDIAN"):
    '''Print all data of devices
    devType specifies how to data should be sperated. Allowed types are spms and myAir
    data must be a string of hexadecimal values'''
    
    devType = devType.upper()
    endian = endian.upper()
    
    
    if endian == "LITTLE_ENDIAN":
        # Convert unicode to list (via string)
        data = list(str(data))
        print(data)
        
        # Convert to big endian
        for i in range(0, len(data), 4):
            tmp           = data[i:i+2]
            data[i:i+2]   = data[i+2:i+4]
            data[i+2:i+4] = tmp
        
        endian = "BIG_ENDIAN"
        
        # Convert back to string
        data = ''.join(data)
    
    if endian == "BIG_ENDIAN":
        if devType == "SPMS" or devType == "MYAIR":
            
            print("Manufactures specific size    = %s" % data[0:2])   # sz = 1 byte
            print("AD type manufacture specific  = %s" % data[2:4])   # sz = 1
            
            print("Company ID                    = %s" % data[4:8])   # sz = 2
            
            print("Temperature ('C)       (x100) = %s" % data[8:12])  # sz = 2
            print("Humidity (%%RH)         (x100) = %s" % data[12:16]) # sz = 2
            print("Pressure (hPa)                = %s" % data[16:20]) # sz = 2
            
            if devType == "SPMS":
                print("Battery voltage (mV)   (/ 20) = %s" % data[20:22]) # sz = 1
                
                print("Status register               = %s" % data[22:24]) # sz = 1
            
                print("Airlfow (mm/s)                = %s" % data[24:28]) # sz = 2
                print("Is ready                      = %s" % data[28:30]) # sz = 1
            elif devType == "MYAIR":
                print("Device specific data          = %s" % data[24:]) # sz = device specific
##            temperature = float(int(data[8:12], 16))/100
##            humidity = float(int(data[12:16], 16))/100
##            batV = float(int(data[20:22], 16))*20
            send_data_to_database(data)
            database_data = local_database.return_data()
            for result in database_data:
                date = str(result[6].date())
                time = str(result[6].time())
                temperature = float(result[1])/100
                humidity = float(result[2])/100
                batV = float(result[3])*20
                airflow = float(result[4])
                pressure = float(result[5])
                spms_mqtt_client = spms_cloud_control.spms_mqtt_init()
                flag = 0
                
                while(1):
                    if (spms_mqtt_client != False):
                        flag = 1
                        try:
                            spms_cloud_control.spms_mqtt_send_data(spms_mqtt_client, temperature, humidity, pressure, batV, airflow, date, time)
                            sleep(1)
                            
                        except:
                            break
                    else:
                        break

                if flag == 1:
                    local_database.remove_data(result[0])
                    flag = 0
                
##                    if (spms_mqtt_client != False):
##                        try:
##                            spms_cloud_control.spms_mqtt_send_data(spms_mqtt_client, temperature, humidity, pressure, batV, airflow, date, time)
##                            sleep(1)
##                        except:
##                            break
##                    else:
##                        break
            
            
            
    return

def send_data_to_database(data):
    temperature = int(data[8:12], 16)
    humidity = int(data[12:16], 16)
    batV = int(data[20:22], 16)
    pressure = int(data[16:20], 16)
    status = int(data[22:24], 16)
    airflow = int(data[24:28], 16)
    local_database.insert_data(temperature, humidity, batV, airflow, pressure)
    
