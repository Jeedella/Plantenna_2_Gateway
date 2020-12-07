###############################################################
# main_control.py                                             #
# author:   Frank Arts                                        #
# date:     December 7th, 2020                                #
# version:  1.4                                               #
#                                                             #
# version info:                                               #
# - Update support for notifictions                           #
#                                                             #
# NOTES:                                                      #
# - Mesh networks are not supported                           #
###############################################################

# import
from bluepy.btle import DefaultDelegate
from ble_network_control import BLE_network
import sys, time, datetime

# global varibles
network_ID      =  "my_first_ble_network"

# functions
def readBLEcharacteristics(ble_network, peripheral = None, service_uuid = None, characteristic_uuid = None):
    # Print date and time
    print("READ")
    dt = datetime.datetime.now()
    print(dt.strftime("%Y %B %d, %X"))
    
    # Read and print characteristics
    ble_network.read_characteristics(peripheral, service_uuid, characteristic_uuid)
    
def writeBLEcharacteristics(ble_network, value, peripheral = None, service_uuid = None, characteristic_uuid = None):
    # Print date and time
    print("WRITE")
    dt = datetime.datetime.now()
    print(dt.strftime("%Y %B %d, %X"))
    
    # Read and print characteristics
    ble_network.write_characteristics(value, peripheral, service_uuid, characteristic_uuid)


# main funciton
def main(argv):
    # Read command input
    local_device_name = None
    if len(argv) == 1:
        device_type = "spms_device"
        print("device type was not specified, 'spms_device' will be used")
        print("(specify device type with: sudo python %s <device type>)" % __file__)
        print('')
    else:
        device_type = argv[1]
        print("User defined device type '%s' will be used" %device_type)
        print('')

    # Print date and time
    dt = datetime.datetime.now()
    print(dt.strftime("%Y %B %d, %X"))

    try:
        # Initialize my_ble_network and timer
        scan_time = 10.0
        my_ble_network = BLE_network(network_ID, device_type, scan_time)
        
        # check if dictionary of peripherals is empty
        if not bool(my_ble_network.get_peripherals()):
            print("Dictionary of peripherals is empty.")
            exit()
        
        
        prevTime_read = time.time()
        prevTime_write = prevTime_read
        
              
        # Read all characteristics
        readBLEcharacteristics(my_ble_network)
        
        p_peripherals = my_ble_network.get_peripherals()
        
        #enable notify
        timeout = 5.0
        my_ble_network.enable_notifications(peripheral = p_peripherals, timeout = timeout)
        

        while 1:
            for i in range(len(p_peripherals)):
                # test notify
                if p_peripherals[i].waitForNotifications(timeout):
                    # handlenotification was called
                    continue;
                print("Waiting...")

            # read all characteristics
            currTime = time.time()
            
            # Read multiple times within 10 seconds (= update time of sensor in nodes)
            if currTime - prevTime_read >= 30:
                # Read BLE characteristics
                readBLEcharacteristics(my_ble_network)#, None, "1a310701-63b2-0795-204f-1dda0100d29d", "1a310702-63b2-0795-204f-1dda0100d29d")
                
                # Update prevTime for reading
                prevTime_read = currTime
                
            '''
            # Write
            if currTime - prevTime_write >= 15: # For testing: write every 15 seconds
                # Write 0xAA to BLE characteristic
                writeBLEcharacteristics(my_ble_network, "\x3A", None, "1a310701-63b2-0795-204f-1dda0100d29d", "1a310702-63b2-0795-204f-1dda0100d29d")
                
                # Update prevTime for writing
                prevTime_write = currTime
            '''
            
                
    finally:
        print('')
        print('')
        
        try:
            # Disable notifications for all peripherals
            print("Disabling notifications...")
            my_ble_network.enable_notifications(enable = False)
        finally:
            pass
        
        # Goodbye
        print("Goodbye!")
        print("Disconnecting...")


if __name__ == "__main__":
    main(sys.argv)
