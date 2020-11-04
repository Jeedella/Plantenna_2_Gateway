# Project Plant Sensing System - Raspberry Pi Gateway - local storage
Update README

## Current status
- Connection between NRF52 and Raspberry Pi has been fully established and tested. Any program that utilizes Bluetooth LE loaded to the NRF52 can be controlled by the Raspberry Pi as long as the correct UUID's are used in the python code. Connecting the Pi to the AWS IoT server has also been proved successfull, but controlling the NRF52 through connection with the Pi on AWS could not be achieved.

## To-do list
- Research into how to achieve control over the NRF52 through the AWS IoT server using the Pi as a gateway. The file "NRF52Rpi_BLE_ChargeCapModel_IoT.py" is the code thought to be able to achieve this, but failed. It was loaded onto AWS, connection with the Pi was established, but no response came from the pi in the shape of messages, nor did the NRF52 indicate connection was being made with the Pi. The file is an attempt at integrating both the basic AWS readout code (greengrassHelloWorld) and the ChargeCapModel pi code into one. (see IoT repo of this project for more info).
