###########################################################
# Version 1.1                                             #
# Use python 2, not python 3                              #
# Usable for ble standard and own defined UUIDs           #
# Purpose: Scan and connect to specific device            #
#          and show its services and characteristics      #
# Order:   0) User can specify a specific device name     #
#          1) Scan for available devices                  #
#          2) Select specific device (automatically)      #
#          3) Aks user to connect to this device          #
#          4) Print services and characteristics          #
#          5) Disconnect from device                      #
# NOTE: Writing is not yet supported                      #
# Updates in version 1.1:                                 #
# - User can specify (but is not mandatory to do so)      #
#   a specific device name he wants  to connect with:     #
#   sudo python scan_and_connect_V1.1.py <device address> #
#   If de user doesn't specify a device, the default      #
#   device name will be "Nordic_Blinky"                   #
# - Create function for printing all services,            #
#   characteristics and their permission(s) (i.e. READ)   #
###########################################################

# Import bluepy
from bluepy.btle import Scanner, DefaultDelegate
from bluepy.btle import UUID, Peripheral, AssignedNumbers
import binascii, sys

# define raw_input as input for python 3
# NOTE: Don't use python 3, because binascii doens't work
if sys.version_info[0] == 3:
    raw_input = input


# my dictionary of UUIDs (services and characteristics)
names = {
    ## Services ##
    # UUID                                  Service name
    "00001523-1212-efde-1523-785feabcd123": "Button service",
    "00001623-1212-efde-1523-785feabcd123": "LED service",
    
    
    ## Tasks/Characteristics ##
    # UUID                                  Taks name
    "00001524-1212-efde-1523-785feabcd123": "Button task",
    "00001624-1212-efde-1523-785feabcd123": "LED task",
    
    
    ## Others ##
    # UUID                                  Taks name
    "1a310000-63b2-0795-204f-1dda0100d29d": "MySensor Broadcast",
    "1a310000-63b2-0795-204f-1dda0100d29e": "MySensor Task"
}

###############
### Classes ###
###############

# Class to save devices
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device %s" % dev.addr)
        elif isNewData:
            print("Received new data from %s" % dev.addr)


#################
### Functions ###
#################

# Scan for ble devices
def scan_for_ble_devices(scan_time = 10.0):
    scanner = Scanner().withDelegate(ScanDelegate())
    sc_devices = scanner.scan(scan_time)    # Scan for specified time (in seconds) default = 10.0 seconds

    # Variables for copies of MAC_addr and device of correct device
    se_device = None
    
    for dev in sc_devices:
        valid_device = False
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))

        # Display all adtype, desc and value of current device
        for (adtype, desc, value) in dev.getScanData():
            print("  %s    %s = %s" % (hex(adtype), desc, value))
            if desc == "Complete 128b Services":
                button_service_uuid = value
                print(value)
                print("got UUI")
            if desc == "Complete Local Name" and value == local_device_name:
                valid_device = True;    # Valid device is found (works only for the first device called "Nordic_Blinky"
                print("found!")
                se_device = dev

        # save + print correct device address
        if valid_device:
            print("MAC address valid device: %s\n" %  dev.addr)
        else:
            print("Not a valid device!\n")

    return se_device


# Print device's services and characteristics
def print_device_services_and_characteristics(p_device, local_device_name = "Nordic_Blinky"):
    # List all services and characteristics
    # NOTE for c-code: Only displayed when service is advertised (advertising_init() and initialized (services_init()) in nRF52DK's main.c
    print('')
    # Print all services with UUID, handleStart and handleEnd (type = instance => field of a class)
    print("Services and Charactertic UUIDs of device '%s':" % local_device_name)

    for se_service in p_device.getServices():
        # Print services
        print("Service:")
        uuid = se_service.uuid
        u_service_uuid = UUID(uuid)
        name = u_service_uuid.getCommonName()    # Check standard UUIDs
        name = names.get(name, name)             # Check in my UUIDs
        print(name)
        print("(uuid=%s)" %uuid)

        # Print characteristics
        print("    Characteristics:")
        chars = False                # More than 1 characteristic
        for ch_characteristic in se_service.getCharacteristics():    # Create object of characteristic class (for every characteristic in se_ object of service class)
            chars = True
            uuid = ch_characteristic.uuid          # Read UUID (value)
            u_chars_uuid = UUID(uuid)              # Create ojbect of UUID class
            name = u_chars_uuid.getCommonName()    # Get UUID name (string)
            name = names.get(name, name)
            print("    %s" %name)
            print("      (uuid=%s)" %uuid)

            # Show properties:
            print("      %s" %ch_characteristic.propertiesToString())

            # Save device name characteristic
            if(name.lower() == "device name"):
                if(ch_characteristic.supportsRead()):
                    device_name = ch_characteristic.read()
                else:
                    print("ERROR: %s is not readable" %ch_characteristic)
            if(name == "MySensor Task"):
                if(ch_characteristic.supportsRead()):
                    # Characteristic is readable => Read + print value
                    str_in = ch_characteristic.read()
                    print("        Current value: %s" % binascii.b2a_hex(str_in))

                    print("        Writing not yet supported")
                    # Ask user what to write on the 2 LSBs of this characteristic
                    #chars = raw_input("Write on the 2 LSBs: 0x")
                    #print("%s will be written to '%s'" % (chars[:2], name))
                    #ch_characteristic.write(chars[:2])

                    # Read+print characteristic again
                    #str_in = ch_characteristic.read()
                    #print("New value of '%s' is: %s " % (name, binascii.b2a_hex(str_in)))
                else:
                    # Not readable
                    print("ERROR: %s is not readble" %ch_characteristic)

        if (chars is False):
            print("    n/a")
        print('')



#################
### Main code ###
#################
if __name__ == "__main__":
    # Read command input
    if len(sys.argv) == 1:                       #if device_name is None:
        local_device_name = "Nordic_Blinky"
        print("device name was not specified, 'Nordic_Blinky' will be used")
        print("(specify device name with: sudo python scan_and_connect_V1.1.py <device name>)")
        print('')
    else:                                        #else device_name is given by user
        local_device_name = sys.argv[1]
        print("User defined device name '%s' will be used" %local_device_name)
        print('')


    # Scan and display all device addresses, services and values
    scan_time = 10.0
    se_device = scan_for_ble_devices(scan_time)
    
    # If a valid device is found, ask user to connect
    if se_device is None:    # No valid device found, so end of code
        print("No valid devices found (searched for device name: '%s')" %local_device_name)
        print("Goodbye!")
        exit()
    else:                   # Valid device found, so aks if user wants to connect to it
        response = raw_input("Do you want to connect to device with MAC address %s? [y/N] " % se_device.addr).lower()
        if response == "y" or response == "yes":    # User accepted connection -> contitnue code
            print("Connecting to device with MAC address %s" % se_device.addr)
        else:                                       # User declined connetion -> end of code
            print("You did not connect to device '%s' with MAC address %s" %(local_device_name, se_device.addr))
            print("Goodbye!")
            exit()

    # Connnect to device
    p_device = Peripheral(se_device.addr, se_device.addrType)
    device_name = None

    try: # Connected to device #
        device_name = print_device_services_and_characteristics(p_device, local_device_name)
    finally: # Connected to device #
        print("No further code made. Disconnecting...")
        # Alwasy disconnect when done
        p_device.disconnect()
        if(device_name == None):
            device_name = "device"
        print("Disconnected from '%s' (MAC address: %s)" %(device_name, p_device.addr))
        print("Goodbye!")
