# Python program to read cleaned json file and process data
import json

import pandas as pd


# Load the JSON data from file
with open('cleaned.json') as f:
    data_in = json.load(f)

# Iterating through the json
# list

# for i in range(1,10):
# 	print(i)

# data is a dictionary containing all points for 400 days.
# The data for each day is stored in its own list called points.
data = data_in['tides']['dataConfig']['series']['groups']



print(len(data[0]['points']))

print(data[0]['points'][1])

# for i in data[0]['points']:
#     print(data[0]['points'][2])

print(pd.to_datetime(int(data[1]['points'][5]['x']), utc=True, unit='s'))



# Closing file
f.close()
