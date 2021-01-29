# Project Plant Sensing System - Raspberry Pi Gateway - local storage
In this release we use a mysql database as local storage. The mysql database stores the data read through BLE from the NRF, and stores it on a database.
If there is connection to the cloud, the data stored on the database is then pushed to the cloud, and afterwards deleted from the database. 

before installing anything remember to run 
```
sudo apt update
sudo apt upgrade
```


## Current status
The current status is getting the database working on pi's without problems and describing the step by step to getting it working.

## To-do list
- Update README2.0 for database
- Get database working on other rpi's
- implement database workings
