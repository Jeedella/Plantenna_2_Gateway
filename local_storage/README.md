# Project Plant Sensing System - Raspberry Pi Gateway - local storage
In this release we use a mysql database as local storage. The mysql database stores the data read through BLE from the NRF, and stores it on a database.
If there is connection to the cloud, the data stored on the database is then pushed to the cloud, and afterwards deleted from the database. 

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




## Current status
The current status is getting the database working on pi's without problems and describing the step by step to getting it working.

## To-do list
- Update README2.0 for database
- Get database working on other rpi's
- implement database workings
