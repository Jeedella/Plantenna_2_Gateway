# Import bluepy
from bluepy.btle import Scanner, DefaultDelegate
from bluepy.btle import UUID, Peripheral

# Local functions
def print_devices_desc_and_value(dev):
    p_device = None
    for dev in p_devices:
        valid_device = False
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))

        # Display all adtype, desc and value of current device
        for (adtype, desc, value) in dev.getScanData():
            print("  %s    %s = %s" % (hex(adtype), desc, value))
            if desc == "Complete 128b Services":
                button_service_uuid = value
                print("got UUID")
            if desc == "Complete Local Name" and value == "Nordic_Blinky":
                valid_device = True;    # Valid device is found (works only for the first device called "Nordic_Blinky"
                print("found!")
                p_device = dev

        # save + print correct device address
        if valid_device:
            print("MAC address valid device: %s\n" %  dev.addr)
        else:
            print("Not a valid device!\n")

    return p_device


# Class to save devices
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

# Scan for devices
scanner = Scanner().withDelegate(ScanDelegate())
p_devices = scanner.scan(10.0)    # Scan for 10.0 seconds

# Variables for copies of MAC_addr and device of correct device
p_device = None

# Display all device addresses, services and values
p_device = print_devices_desc_and_value(p_devices)

# If MAC_addr is valid (else), ask if user wants to connect to this device (MAC address of this device is given)
if p_device is None:    # No valid device found, so end of code
    print("No valid devices found")
    print("Goodbye!")
    exit()
else:                   # Valid device found, so aks if user wants to connect to it
    response = raw_input("Do you want to connect to device %s? [y/N] " % p_device.addr).lower()
    if response == "y" or response == "yes":    # User accepted connection -> contitnue code
        print("Connecting to %s" % p_device.addr)
        print("No further code made. Goodbye!")
    else:                                       # User declined connetion -> end of code
        print("You did not connect to %s" % p_device.addr)
        print("Goodbye!")
        exit()

# Print services
for peripheral in p_device.services:
    print str(peripheral)
