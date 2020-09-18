import sys
import binascii
import struct
import time
from bluepy.btle import UUID, Peripheral  
from bluepy import btle

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
    while 1:
     	LedWrite.write(str("\x01"));
      	print ("Led2 on")
     	time.sleep(1)
       	LedWrite.write(str("\x00"));
    	print ("Led2 off")
       	time.sleep(1)
finally:
    Perif.disconnect()
