###############################################################
# control_my_ble_network.py                                   #
# author:   Frank Arts                                        #
# date:     November 5th, 2020                                #
# version:  1.0                                               #
#                                                             #
# version info:                                               #
# - frist version to control my ble network                   #
#                                                             #
# NOTES:                                                      #
# - Mesh networks are not supported                           #
# - Writing to tasks is not yet supported                     #
# -! Must replace line 48. See comment                        #
###############################################################

# import
from bluepy.btle import Scanner, DefaultDelegate, Service
from bluepy.btle import UUID, Peripheral, AssignedNumbers
from bluepy.btle import ADDR_TYPE_PUBLIC, ADDR_TYPE_RANDOM
from ble_network_control import BLE_network
import sys, time

#### network class ####
network_ID      =  "my_first_ble_network"

# Read command input
local_device_name = None
if len(sys.argv) == 1:
    device_type = "spms_device"
    print("device type was not specified, 'spms_device' will be used")
    print("(specify device type with: sudo python ble_network_testing.py <device type>)")
    print('')
else:
    device_type = sys.argv[1]
    print("User defined device type '%s' will be used" %device_type)
    print('')

try:
    # Initialize my_ble_network
    scan_time = 10.0
    my_ble_network = BLE_network(network_ID, device_type, scan_time)

    # read all tasks
    while 1: # Continues loop
        
        # only read "Portable Airflow task" (of every device/peripheral)
        # and only twice within 60 seconds (--> update time of sensor in node is 60 seconds. Update twice in that time to prevent missing information)
        if True: # Every 30 seconds
            my_ble_network.save_tasks(None, "1a310701-63b2-0795-204f-1dda0100d29d", "1a310702-63b2-0795-204f-1dda0100d29d")
            
finally:
    print("Goodbye!")
    print("Disconnecting...")
