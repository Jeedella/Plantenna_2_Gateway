#

from bluepy.btle import Scanner, DefaultDelegate
from ChargeCapModel import charge_cap_model as CCM

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

MAC_addr = None
device = None

for dev in devices:
    valid_device = False
    print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
    for (adtype, desc, value) in dev.getScanData():
        print("  %s    %s = %s" % (hex(adtype), desc, value))
        if desc == "Complete Local Name" and value == "Nordic_Blinky":
            valid_device = True;
            print("found!")
            device = dev
            print(device)
            MAC_addr = dev.addr

    # save + print device address
    if valid_device:
        print("MAC address valid device: %s\n" %  MAC_addr)
    else:
        print("Not a valid device!\n")

if MAC_addr is None:
    print("No valid devices found")
else:
    response = raw_input("Do you want to connect to device %s? [y/N] " % MAC_addr).lower()
    if response == "y" or response == "yes":
        print("Connecting to %s" % MAC_addr)
        CCM(MAC_addr)
    else:
        print("You did not connect to %s" % MAC_addr)
        print("Goodbye!")
