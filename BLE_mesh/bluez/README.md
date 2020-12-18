# Project Smart Plant Monitoring System - Raspberry Pi Gateway - BLE network based on bluez
This README shows the current status of the gateway using bluez, the to-do list and 2 methods of using bluez.\
For the installation of bluez and provisioning of devices refer to the specific readme files (see below).

## Function of Raspberry pi gateway
The Raspberry pi is not be part of the BLE mesh network, but is used as provisioner for the BLE mesh network. This is be done using meshctl of [bluez](bluez.org).
To communicate with the BLE mesh network, there is an other gateway between the Raspberry pi gateway and the BLE mesh network. The Raspberry pi uses standard BLE to communicate with the other gateway. Also, the Raspberry pi is still be used as gateway to the cloud. It is still possible to use the Raspberry pi as gateway for other networks, but will not be further discussed here.\

More information:
- [BLE](../../BLE)
- [Network architecture - standard BLE, BLE mesh and LoRa](../network-architecture_BLE_BLE-mesh_and_LoRa.png)
- [Install bluez](Install_bluez.md)
- [Provisioning](Provisioning.md)

## Current status
- Devices can be provisioned using bluez meshctl; and
- An LED can be controlled on at least 2 nRF52-DKs (both running Zephyr.hex) using meshctl on the raspberry pi. It should be possible to use more.

## To-do list
- Create a script (possably python) to ease the use of provisioning nodes; and
- Research into methods to use the Raspberry pi within the BLE mesh network.

## 2 methods to use bluez
Method 1 bluez meshctl:
- Staring meshctl, as described [here](Provisioning.md); and
- Using bluez as described in Chapter 3 and onwards in ["Tutorial-How-to-set-up-BlueZ_Part2-3.pdf"](Tutorial-How-to-set-up-BlueZ_Part2-3.pdf) and in ["Step-by-step-guide-meshctl-with-Zephyr.pdf"](Step-by-step-guide-meshctl-with-Zephyr.pdf).\
\
Method 2 bluez with python script:
- Using [this library](https://github.com/adafruit/Adafruit_Python_BluefruitLE), as described in [this video](https://www.youtube.com/watch?v=wKZaYKavJsQ).\
\
NOTE: Other methods/libraries/etc. may also be available, but method 1 is used in the current version of this project.
