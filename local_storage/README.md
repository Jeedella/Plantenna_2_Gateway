# Project Plant Sensing System - Raspberry Pi Gateway - local storage
In this release we use a mysql database as local storage. The mysql database stores the data read through BLE from the NRF, and stores it on a database.
If there is connection to the cloud, the data stored on the database is then pushed to the cloud, and afterwards deleted from the database. 
note that this release is for python 2.7

before installing anything remember to run 
```
sudo apt update
sudo apt upgrade
```

afterwards run the following 2 commands to install the database
```
sudo apt install mariadb-server
sudo mysql_secure_installation
```
follows the prompts and make sure to change to password to 'plantenna'

after installing the database the user has to log in using the command 
```
sudo mysql -u root -p
```
this will ask the user for the password, in this case being 'plantenna'
note that the text will not show up when typing, as with most linux passwords.

to create the database, run the following(note that when using MySQL you need to finish commands with ';'):
```
create database plantenna
```
to create the table used in this project, run:
```
create table sensor_data (
number int not null auto_increment primary key,
temperature int(3),
humidity int(3),
battery_voltage int(3),
airflow int(3),
pressure int(3)
);
````
the database has now been created, including the necessary columns and their properties
in case you ever want to exit just run ```exit``` or ```quit```

in order to acces the database with python code we need to install a connector. This is done with the command:
```
sudo pip install mysql-connector-python
```

to test local storage run
```
sudo python local_database.py
``` 
if the file is run from python 3 it will not work. The rest of the project has been done with python 2.7 which is the reason the code
for the local database is also in python 2.7

Note that to test everything you must install all dependencies from cloud control (BME and SMBUS2), and main_control and ble_network_control(bluepy)
To test everything working together, the files necessary are ble_network_control.py, local_database.py, main_control.py, and spms_cloud_control.py
make sure the key etc in spms_cloud_control.py is correct,
in local_database.py make sure the user, password and host are correct. 
then run ```sudo python main_control.py ``` followed by the name of the NRF, in this case 'SPMS N01'. Note if it contains spaces it has to be written as string

## Current status
The current status is a working database. The data received from NRF's are sent to the database, and if the pi connects to the cloud, 
all data in the database is sent to the cloud and deleted from the database. 
if there is no connection, the data stays in the database, readdy to be sent to the cloud when connection is restored.

## To-do list
-set a protocol for BLE mesh
 -create the interfacing for BLE mesh
 improve LoRa interface
