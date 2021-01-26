# Author: Omar Mhaouch
# Date: 5-1-2021
# Last updated: 26-01-2021

# This script is used to test out the JSON config file functionality.
# Not used in the actual SPMS script.

import json

# first import the data from the config file
with open("config.json", 'r') as config_file:
    data = json.load(config_file)

# to read a single object use the following:
print(data['host'])

# to read a nested object, use the following:
print(data['PA001']['ACCESSTOKEN'])

