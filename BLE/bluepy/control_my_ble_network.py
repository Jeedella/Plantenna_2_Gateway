###############################################################
# control_my_ble_network.py                                   #
# author:   Frank Arts                                        #
# date:     November 6th, 2020                                #
# version:  1.1                                               #
#                                                             #
# version info:                                               #
# - Reading tasks is only executed every 30 seconds.          #
# - Add writing tasks.                                        #
# - Add current day and time when tasks are read.             #
#                                                             #
# NOTES:                                                      #
# - Mesh networks are not supported                           #
###############################################################

# import
from ble_network_control import BLE_network
import sys, time, datetime

# Varibles
network_ID      =  "my_first_ble_network"

# Functions
def readBLEtasks(peripheral = None, service_uuid = None, task_uuid = None):
    # Print date and time
    print("READ")
    dt = datetime.datetime.now()
    print(dt.strftime("%Y %B %d, %X"))
    
    # Read and print tasks
    my_ble_network.save_tasks(peripheral, service_uuid, task_uuid)
    
def writeBLEtasks(value, peripheral = None, service_uuid = None, task_uuid = None):
    # Print date and time
    print("WRITE")
    dt = datetime.datetime.now()
    print(dt.strftime("%Y %B %d, %X"))
    
    # Read and print tasks
    my_ble_network.write_tasks(value, peripheral, service_uuid, task_uuid)

# Read command input
local_device_name = None
if len(sys.argv) == 1:
    device_type = "spms_device"
    print("device type was not specified, 'spms_device' will be used")
    print("(specify device type with: sudo python %s <device type>)" % __file__)
    print('')
else:
    device_type = sys.argv[1]
    print("User defined device type '%s' will be used" %device_type)
    print('')
    
# Print date and time
dt = datetime.datetime.now()
print(dt.strftime("%Y %B %d, %X"))

try:
    # Initialize my_ble_network and timer
    scan_time = 10.0
    my_ble_network = BLE_network(network_ID, device_type, scan_time)
    prevTime_read = time.time()
    prevTime_write = prevTime_read
    
    # Read all tasks
    readBLEtasks()
    
    p_peripherals = my_ble_network.get_peripherals()
    
#     
#     service_uuid = []
#     task_uuid =[]
#     
#     for p in p_peripherals:
#         
#         for se_service in p.getServices():
#             if se_service.uuid == "1a310701-63b2-0795-204f-1dda0100d29d":
#                 service_uuid.append(se_service.uuid)
#             
#             for ch_task in se_service.getCharacteristics():
#                 task_uuid.append(ch_task.uuid)

    # read all tasks
    while 1: # Continues loop
        currTime = time.time()
        
        
        # Read multiple times within 60 seconds (= update time of sensor in nodes)
        if currTime - prevTime_read >= 10:
            # Read BLE tasks
            readBLEtasks(None, "1a310701-63b2-0795-204f-1dda0100d29d", "1a310702-63b2-0795-204f-1dda0100d29d")
            
            # Update prevTime for reading
            prevTime_read = currTime
            
        
        # Write
        if currTime - prevTime_write >= 15: # For testing: write every 15 seconds
            # Write 0xAA to BLE task
            writeBLEtasks("\x3A", None, "1a310701-63b2-0795-204f-1dda0100d29d", "1a310702-63b2-0795-204f-1dda0100d29d")
            
            # Update prevTime for writing
            prevTime_write = currTime
        
            
finally:
    print("Goodbye!")
    print("Disconnecting...")
