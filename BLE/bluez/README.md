# Project Plant Sensing System - Raspberry Pi Gateway - BLE network based on bluez
This README shows how to install the important libraries, how to start bluez meshctl, and the possible problems and solutions with bluez.\
In addition, the current status of the gateway using bluez, the to-do list and 2 methods of using bluez, are added below.

## Installing bluez
Follow the guide "Tutorial-How-to-set-up-BlueZ.pdf" to install bluez.

## How to start bluez meshctl
When bluez is installed correctly, meshctl can be found in the folder bluez-5.50/mesh. Please replace "5.50" by your version of bluez.
You can check your version of bluez and meshctl with the command:
```bash
bluetoothd -v
meshctl -v
```

Type the following command to start meshctl:
```bash
meshctl
```

The following should appear on the terminal:
```bash
pi@raspberrypi:~/bluez-5.50/mesh $ meshctl
[meshctl]# 
```
If any problems occur, please refer to the [Possible problems and solutions with bluez](#-Possible-problems-and-solutions-with-bluez).\
Chapter 3 and onwards in the guide "Tutorial-How-to-set-up-BlueZ_Part2-3.pdf" shows how to use the bluez meschtl. Use the nRF52-DK and run the program Zephyr.hex on it. This program spits out the provisioning key on a serial terminal, like [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html). The nRF52-DK's micro-USB input should be connected to the USB input of the PC (or any other device with a serial monitor).
In addition, a step-by-step guide with pictures ("Step-by-step-guide-meshctl-with-Zephyr.pdf") is also provided. The program Zephyr.hex was running on the nRF5-DK and PuTTY was installed on a Windows 10 laptop.

## Possible problems and solutions with bluez
The following list gives all possible problems that could occur after installing or after changing some files from bluez:

1. local_node.json\
When trying to start meshctl and this message appears:
```bash
failed to parse local node configuration file local_node.json
```
something went wrong during step 3 of installing bluez. Please repeat step 3.0 up to step 3.5 and the problem should be solved. If not, please redo steps 2.2, 2.5 - 3.5 (re-install bluez-5.50 and update kernel) and try again (be user to remove the bluez-5.50 directory first). If it still fails, try to redo the entire guide (first remove all).

## Current status of the gatway using bluez
- bluez meshctl on the Raspberry Pi is working with multiple nRF52-DKs. It was tested with 3 different devices (all running Zephyr.hex), but it should be possible to use more.
- bluez can also be used by writing a python script, instead of running meshctl. Watch [this video](https://www.youtube.com/watch?v=wKZaYKavJsQ) for a possible library you can use for this. The library can be found in the description of the video or with [this link](https://github.com/adafruit/Adafruit_Python_BluefruitLE).

## To-do list
bluez:
- Research into the specific meaning and syntax of steps 10 to 13 in the bluez mesctl with Zephyr guide; and
- Research into the useability of all other commands from meshctl (after starting meshctl type 'help' in all menus).

# 2 methods to use bluez
Method 1 bluez meshctl:
- Staring meshctl, as described in [How to start bluez meshctl](#-How-to-start-bluez-meshctl); and
- Using bluez as described in Chapter 3 and onwards of "Tutorial-How-to-set-up-BlueZ_Part2-3.pdf.pdf" and in "Step-by-step-guide-meshctl-with-Zephyr.pdf".\
\
Method 2 bluez with python script:
- Using [this library](https://github.com/adafruit/Adafruit_Python_BluefruitLE), as described in [this video](https://www.youtube.com/watch?v=wKZaYKavJsQ).\
\
NOTE: Other methods/libraries/etc. may also be available.
