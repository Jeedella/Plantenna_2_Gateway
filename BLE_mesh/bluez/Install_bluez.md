# Project Smart Plant Monitoring System - Raspberry Pi Gateway - BLE network based on bluez - Installing bluez and dependencies
## Installing bluez
Install bluez using the commands in the steps below. These steps are based on: ["Tutorial-How-to-set-up-BlueZ.pdf"](Tutorial-How-to-set-up-BlueZ.pdf).\
Note that v5.50 is used during development of this project. If you whish to use other version of bluez, check the available versions on [the bluez website](http://www.bluez.org/). With other version of bluez, it may be possible that the json-c and ell version must change as well. Note that meshctl must be present in your version of bluez.
1. Install dependencies of bluez:
```
sudo apt-get install -y git bc libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev autoconf
```
2. Install json-c
```
cd ~
wget https://s3.amazonaws.com/json-c_releases/releases/json-c-0.13.tar.gz
tar -xvf json-c-0.13.tar.gz
cd json-c-0.13/
./configure --prefix=/usr --disable-static && make
sudo make install 
```

3. Install ell for bluez v5.50
```
cd ~
wget https://mirrors.edge.kernel.org/pub/linux/libs/ell/ell-0.6.tar.xz
tar -xvf ell-0.6.tar.xz
cd ell-0.6/
sudo ./configure --prefix=/usr
sudo make
sudo make install
```

4. Get bluez v5.50 source code
Rplace 5.50 with your prefered version.
```
cd ~
wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.50.tar.xz
tar -xvf bluez-5.50.tar.xz
cd bluez-5.50/
```

5. Compile and install bluez
```
./configure --enable-mesh --prefix=/usr --mandir=/usr/share/man --sysconfdir=/etc --localstatedir=/var
make
sudo make install
```

6. Create a link from the old bluetoothd to the new one
```
sudo cp /usr/lib/bluetooth/bluetoothd /usr/lib/bluetooth/bluetoothd-543.orig
```

7. Check version of bluetoothd and meshctl
The versions should be the same and correspond to the installed version in step 3 above.
```
sudo ln -sf /usr/libexec/bluetooth/bluetoothd /usr/lib/bluetooth/bluetoothd
sudo systemctl daemon-reload
bluetoothd -v
meshctl -v
```

8. Rebuild the kernel for bluez v5.50\
8.1. Install kernal building dependencies
```
sudo apt-get install -y git bc bison flex libssl-dev
```
8.2. Check out building tool and souce code
```
cd ~
wget https://github.com/raspberrypi/linux/archive/raspberrypi-kernel_1.20190709-1.tar.gz
tar -xvf raspberrypi-kernel_1.20190709-1.tar.gz
```
8.3. Configure the kernel
```
cd ~
cd ./linux-raspberrypi-kernel_1.20190709-1/
```
For Raspberry pi 2, 3, 3+ and compute module 3:
```
KERNEL=kernel7
make bcm2709_defconfig
make menuconfig
```
For Raspberry pi 4:
```
KERNEL=kernel7l
make bcm2711_defconfig
make menuconfig
```
In the pop-up menu, select the folowing items:
- Cryptographic API → CMAC support
- Cryptographic API → User-space interface for hash algorithms
- Cryptographic API → User-space interface for symmetric key cipher algorithms
8.4. Build and install the kernel, modules, and device tree blobs
This step may take 2 to 3 hours.
```
make -j4 zImage modules dtbs
sudo make modules_install
sudo cp arch/arm/boot/dts/*.dtb /boot/
sudo cp arch/arm/boot/dts/overlays/*.dtb* /boot/overlays/
sudo cp arch/arm/boot/dts/overlays/README /boot/overlays/
sudo cp arch/arm/boot/zImage /boot/$KERNEL.img
sudo reboot
```

9. Verify the kernel installation
```
uname -a
```
Check if the date and time correspond to the build of the kernel.
