######################################################
# Version 1                                          #
# Use python 2, not python 3                         #
# Usable for ble standard and own defined UUIDs      #
# Purpose: Scan and connect to specific device       #
#          and show its services and characteristics #
# Order:   1) Scan for available devices             #
#          2) Select specific device (automatically) #
#          3) Aks user to connect to this device     #
#          4) Print services and characteristics     #
#          5) Disconnect from device                 #
# NOTE: Writing is not yet supported                 #
######################################################

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
    # UUID                                  # UUID name
    "1a310000-63b2-0795-204f-1dda0100d29d": "MySensor Broadcast",
    "1a310000-63b2-0795-204f-1dda0100d29e": "MySensor Task"
}

# Local functions
def print_devices_desc_and_value(dev):
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
            if desc == "Complete Local Name" and value == "Zephyr plantenna node V1":
                valid_device = True;    # Valid device is found (works only for the first device called "Nordic_Blinky"
                print("found!")
                se_device = dev

        # save + print correct device address
        if valid_device:
            print("MAC address valid device: %s\n" %  dev.addr)
        else:
            print("Not a valid device!\n")

    return se_device


# Class to save devices
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device %s" % dev.addr)
        elif isNewData:
            print("Received new data from %s" % dev.addr)

# Scan for devices
scanner = Scanner().withDelegate(ScanDelegate())
sc_devices = scanner.scan(10.0)    # Scan for 10.0 seconds

# Variables for copies of MAC_addr and device of correct device
se_device = None

# Display all device addresses, services and values
se_device = print_devices_desc_and_value(sc_devices)

# If MAC_addr is valid (else), ask if user wants to connect to this device (MAC address of this device is given)
if se_device is None:    # No valid device found, so end of code
    print("No valid devices found")
    print("Goodbye!")
    exit()
else:                   # Valid device found, so aks if user wants to connect to it
    response = raw_input("Do you want to connect to device with MAC address: %s? [y/N] " % se_device.addr).lower()
    if response == "y" or response == "yes":    # User accepted connection -> contitnue code
        print("Connecting to device with MAC address %s" % se_device.addr)
    else:                                       # User declined connetion -> end of code
        print("You did not connect to device with MAC address %s" % se_device.addr)
        print("Goodbye!")
        exit()

# Connnect to device
p_device = Peripheral(se_device.addr, se_device.addrType)
device_name = None

try: # Connected to device #
    # List all services and characteristics
    # NOTE for c-code: Only displayed when service is advertised (advertising_init() and initialized (services_init()) in nRF52DK's main.c
    print('')
    # Print all services with UUID, handleStart and handleEnd (type = instance => field of a class)
    print("Services and Charactertic UUIDs")

#    services = p_device.getServices()
#    services.append(p_device.getServiceByUUID("1a310000-63b2-0795-204f-1dda0100d29d"))

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
finally: # Connected to device #
    print("No further code made. Disconnecting...")
    # Alwasy disconnect when done
    p_device.disconnect()
    if(device_name == None):
        device_name = "device"
    print("Disconnected from '%s' (MAC address: %s)" %(device_name, p_device.addr))
    print("Goodbye!")
