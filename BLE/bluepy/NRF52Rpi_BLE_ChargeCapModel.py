import sys
import binascii
import struct
import time
import math
from bluepy.btle import UUID, Peripheral


def charge_cap_model(MAC_addr):

    # Check if MAC address was given
    if MAC_addr is None:
        raise TypeError("Must pass MAC address.")

    Discharge = 0
    button_service_uuid = UUID('000015231212efde1523785feabcd123')
    button_char_uuid    = UUID('000015241212efde1523785feabcd123')

    led_service_uuid = UUID('000016231212efde1523785feabcd123')
    led_char_uuid = UUID('000016241212efde1523785feabcd123')

    p = Peripheral(MAC_addr, "random")
    B_service=p.getServiceByUUID(button_service_uuid)
    L_service=p.getServiceByUUID(led_service_uuid)
    volt = 0.0
    lim = 45
    Pos = 0
    Neg = 0
    Down = 1
    Up = 1

    try:
        ch = B_service.getCharacteristics(button_char_uuid)[0]
        LedWrite = L_service.getCharacteristics(led_char_uuid)[0]
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
                time.sleep(0.5)

    finally:
        p.disconnect()


if __name__ == "__main__":
    # Check if MAC address was given
    if len(sys.argv) < 2:                       #if MAC_addr is None:
        raise TypeError("Must pass MAC address.")

    # No error
    charge_cap_model(sys.argv[1])
