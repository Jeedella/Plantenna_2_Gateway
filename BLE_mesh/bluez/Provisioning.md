# Project Smart Plant Monitoring System - Raspberry Pi Gateway - BLE mesh network based on bluez - Provisioning
## How to use bluez meshctl for provisioning
When bluez is installed correctly, meshctl can be found in the folder bluez-5.50/mesh. Please replace 5.50 with your version of bluez.\
For more details on these steps, see the step-by-step guide with pictures ["Step-by-step-guide-meshctl-with-Zephyr.pdf"](Step-by-step-guide-meshctl-with-Zephyr.pdf). The program Zephyr.hex was running on the nRF5-DK and PuTTY was installed on a Windows 10 laptop.
1. Check bluez version
```
bluetoothd -v
meshctl -v
```
2. Start meshctl
```
cd ~
cd bluez-5.50/mesh
meshctl
```
If no error pops up, press enter to reveal the meshctl command line ([meshctl]#):
```
pi@raspberrypi:~/bluez-5.50/mesh $ meshctl
[meshctl]# 
```
If any problems occur here, please refer to the [Possible problems and solutions with bluez](#-Possible-problems-and-solutions-with-bluez).\
Chapter 3 and onwards in the guide "Tutorial-How-to-set-up-BlueZ_Part2-3.pdf" shows how to use the bluez meschtl. Use the nRF52-DK and run the program Zephyr.hex on it. This program spits out the provisioning key on a serial terminal, like [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html). The nRF52-DK's micro-USB input should be connected to the USB input of the PC (or any other device with a serial monitor).
In addition, a step-by

3. Discover uprovisioned devices
```
discover-unprovisioned on
```

4. Provision a device
Replace \<Device UUID\> with the corresponding device UUID of your device.\
The Device UUID should look similar to this: 34ab739aa2f000000000000000000000
```
provision <Device UUID>
```

5. Possible key verification
Only do this when prompted to specify a key. Replace \<key\> with your key.\
This key can be an OOB key or an ASCII key and could be found in the terminal of your device.\
An ASCII key should look similar to this: 851IR7K.
```
<key>
```
After this step, the meshctl command line should look simular to the following.\
The name of your device should be there instead of Zephyr.
```
[Zephyr-Net-0000]
```

## Possible problems and solutions with bluez
The following list gives all possible problems that could occur after installing or after changing some files from bluez:

1. local_node.json\
When trying to start meshctl and this message appears:
```
failed to parse local node configuration file local_node.json
```
something went wrong during the installation. Delete all subdirectories (in the home/pi directory) that were create during the installation and repeat [these](Install_bluez.md) steps.
