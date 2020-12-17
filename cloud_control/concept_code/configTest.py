import json

# first import the data from the config file
with open("config.json", 'r') as config_file:
    data = json.load(config_file)

# to read a single object use the following:
print(data['host'])

# to read a nested object, use the following:
print(data['PA001']['ACCESSTOKEN'])

        