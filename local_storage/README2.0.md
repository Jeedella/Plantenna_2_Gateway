# Project Plant Sensing System - Raspberry Pi Gateway - local storage
in this we have th python files that can be used as an example on how to send data to the database on the pi.
in order for this code to work the user needs to install dependencies on the raspberry pi and create the database and table within the database.

before installing anything it is recommended to run the commands:   sudo apt update
                                                                    sudo apt upgrade
after these 2 commands, possibly taking very long are done, run:
```
sudo apt install mariadb-server
sudo mysql_secure_installation
```

follow the prompts and make sure to change the password. The password used in this example is 'plantenna'

after installing the database the user has to log in using the command 
```bash
sudo mysql -u root -p
```
this will ask the user for the password, in this case being 'plantenna'
note that the text will not show up when typing, as with most linux passwords.

now to create the database, we run the commands(note that in mysql you need to send the ';' for the command to execute):
````
create database plantenna;

use plantenna;

create table Sensor_data (
number int not null auto_increment primary key,
temperature int(3),
humidity int(3),
battery_voltage int(3),
airflow int(3),
pressure int(3)
);
````

now the database is created with the necessary columns. 

To access the database with python code we need to install the mysql connector.
This is done by executing the following commands:
```
sudo pip3 install mysql-connector-python
```
run
```
sudo pip3 search mysql-connector | grep --color mysql-connector-python
sudo pip3 install mysql-connector-python-rf
```
because it may be that the connector has issues accessing the database if not created in this way.



## Current status
- TBD

## To-do list
- Update README
- Add local storage
