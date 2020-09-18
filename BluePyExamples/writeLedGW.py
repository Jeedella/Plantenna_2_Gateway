import json
import logging
import platform
import sys
import binascii
import struct
import time
from bluepy.btle import UUID, Peripheral  
from bluepy import btle

import greengrasssdk

led_service_uuid = btle.UUID('000015231212efde1523785feabcd123')
print led_service_uuid
led_char_uuid = btle.UUID('000015251212efde1523785feabcd123')
print led_char_uuid

if len(sys.argv) != 2:
  print "Fatal, must pass device address:", sys.argv[0], "<device address="">"
  quit()

Perif = btle.Peripheral(sys.argv[1], "random")
print Perif
LedService = Perif.getServiceByUUID(led_service_uuid)
print LedService

try:
    LedWrite = LedService.getCharacteristics(led_char_uuid)[0]
    print LedWrite
    # while 1:
    LedWrite.write(str("\x01"));
    print ("Led2 on")
    time.sleep(1)
    LedWrite.write(str("\x00"));
    print ("Led2 off")
    # time.sleep(1)
finally:
    Perif.disconnect()

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

# Retrieving platform information to send from Greengrass Core
my_platform = platform.platform()

# Counter to keep track of invocations of the function_handler
my_counter = 0

def function_handler(event, context):
    global my_counter
    my_counter = my_counter + 1
    try:
        if not my_platform:
            client.publish(
                topic="hello/world",
                queueFullPolicy="AllOrException",
                payload=json.dumps(
                    {"message": "Hello world! Sent from Greengrass Core.  Invocation Count: {}".format(my_counter)}
                ),
            )
        else:
            client.publish(
                topic="hello/world",
                queueFullPolicy="AllOrException",
                payload=json.dumps(
                    {
                        "message": "Hello world! Sent from Greengrass Core running on platform: {}.".format(my_platform)
                                   + "  Invocation Count: {}".format(my_counter)
                    }
                ),
            )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))
    time.sleep(20)
    return
