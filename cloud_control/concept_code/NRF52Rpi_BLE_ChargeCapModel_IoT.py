import sys
import binascii
import struct
import time
import math
from bluepy.btle import UUID, Peripheral
import json
import logging
import platform

import greengrasssdk

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

# Retrieving platform information to send from Greengrass Core
my_platform = platform.platform()

button_service_uuid = UUID('000015231212efde1523785feabcd123')
button_char_uuid    = UUID('000015241212efde1523785feabcd123')
led_char_uuid = UUID('000015251212efde1523785feabcd123')

if len(sys.argv) != 2:
  print "Fatal, must pass device address:", sys.argv[0], "<device address="">"
  quit()

p = Peripheral(sys.argv[1], "random")
BLService=p.getServiceByUUID(button_service_uuid)
volt = 0.0
lim = 45
Pos = 0
Neg = 0
Down = 1
Up = 1 

ch = BLService.getCharacteristics(button_char_uuid)[0]
LedWrite = BLService.getCharacteristics(led_char_uuid)[0]

# finally:
#    p.disconnect()

def function_handler(event, context):
    try:
        if (ch.supportsRead()):
        while 1:
            val = binascii.b2a_hex(ch.read())
            if (val == "01"):
                if (Down == 1):
                    Pos = 0; 
                    Down = 0;
                    Up = 1;
                Pos = Pos + 1;    
                volt = 24*(1-math.exp(-Pos*0.50));
                Discharge = volt;
            elif (val == "00"):
                if (Up == 1):
                    Neg = 0;
                    Up = 0;
                    Down = 1;
                Neg = Neg + 1;
                volt = Discharge*(math.exp(-Neg*0.50));
                if (Neg >= lim):
                    volt = 0.0;
            print ("{:.6}".format(volt))
            if (volt > 23.95):
                LedWrite.write(str("\x01"));
            else: 
                LedWrite.write(str("\x00"));
        
        if not my_platform:
            client.publish(
                topic="hello/world",
                queueFullPolicy="AllOrException",
                payload=json.dumps(
                    {"counter": .format(volt)}
                ),
            )
        else:
            client.publish(
                topic="hello/world",
                queueFullPolicy="AllOrException",
                payload=json.dumps(
                    {"counter": .format(volt)}
                ),
            )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))
    time.sleep(0.5)
    Timer(10,funtion_handler).start()
    
function_handler()
