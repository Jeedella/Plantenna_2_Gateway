###############################################################
# main_control.py                                             #
# author:   Frank Arts                                        #
# date:     December 31st, 2020                               #
# version:  1.6                                               #
#                                                             #
# version info:                                               #
# - Convert endian of ble data to little-endian               #
#                                                             #
# NOTES:                                                      #
# - Mesh networks are not supported                           #
###############################################################
import local_database
# import
from bluepy.btle import DefaultDelegate
from ble_network_control import BLE_network
import sys, time, datetime

# global varibles
network_ID      = "my_first_ble_network"
p2p             = False
broadcastData   = False

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
    # Get global variables
    global network_ID
    global p2p
    global broadcastData
    
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
    
        # Check if user wants to receive broadcast data
        response = raw_input("Would you like to receive broadcast data? [y/N] ").lower()
        if response == "y" or response == "yes": # Accepted
                print("Broadcast data will be scanned for.")
                broadcastData = True
                
                # check if dictionary of peripherals is empty
                if not bool(my_ble_network.get_peripherals()):
                    print("Dictionary of peripherals is empty.")
                    print("Only broadcast data will be received.")
                    p2p = False;
                else:
                    print("Dictionary of peripherals contains one or mulitple peripherals.")
                    print("Both broadcast data and p2p connection(s) will be used.")
                    p2p = True;
        else: # Declined
            print("You did not want to receive broadcast data.")
            broadcastData = False
            
            # check if dictionary of peripherals is empty
            if not bool(my_ble_network.get_peripherals()):
                print("Dictionary of peripherals is also empty.")
                print("Program will be terminated.")
                p2p = False
                exit()
            else:
                print("Only p2p connection(s) will be used.")
                p2p = True
        
        print('')
        prevTime_read = time.time()
        prevTime_write = prevTime_read
        
        if p2p == True:
            # Read all characteristics
            readBLEcharacteristics(my_ble_network)
            
            p_peripherals = my_ble_network.get_peripherals()
        
            # Enable notifications
            p2p_timeout = 5.0
            my_ble_network.enable_notifications(timeout = p2p_timeout)
        
        if broadcastData == True:
            # Enable receive broadcast data
            my_ble_network.enable_broadcast_data_receive()
            
            # timeout for broadcast data receive
            broadcastData_timeout = 10.0
        
        while 1:
            # Get current time
            currTime = time.time()
            
            if p2p == True:
                # Notifications
                for i in range(len(p_peripherals)):
                    if p_peripherals[i].waitForNotifications(p2p_timeout): #NOTE: system is waiting for ('p2p_timeout' * amount of peripherals) seconds
                        # handlenotification was called
                        continue;
                    
                    print("Waiting...")
                
                # Read
                if currTime - prevTime_read >= 30:
                    # Read BLE characteristics
                    readBLEcharacteristics(my_ble_network) #, None, "1a310701-63b2-0795-204f-1dda0100d29d", "1a310702-63b2-0795-204f-1dda0100d29d")
                    
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
                    
            if broadcastData == True: #NOTE: system is waiting for ('broadcastData_timeout' * amount of peripherals) seconds
                my_ble_network.receive_broadcast_data(timeout = broadcastData_timeout)
            
    finally:
        print('')
        print('')
        
        if p2p == True:
            try:
                # Disable notifications for all peripherals
                print("Disabling notifications...")
                my_ble_network.enable_notifications(enable = False)
            finally:
                pass
        
        if broadcastData == True:
            try:
                # Stop broadcast data receive
                print("Stopping broadcast data receive...")
                my_ble_network.enable_broadcast_data_receive(enable = False)
            finally:
                pass
        
        # Goodbye
        print("Goodbye!")
        print("Disconnecting...")


if __name__ == "__main__":
    main(sys.argv)
