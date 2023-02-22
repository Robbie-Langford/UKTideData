# Python program to read cleaned json file and process data
import json

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots




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



print(data[0]['points'][1])

leak_height = 4.5

x_values = []
y_values = []
y_leak =[]

for j in range(0,399):
    for i in data[j]['points']:
        x_values.append(pd.to_datetime((i['x']), utc=True, unit='s'))
        y_values.append(i['y'])
        if i['y'] > 4.5:
            y_leak.append(0.375*(i['y']-leak_height))
        else:
            y_leak.append(0)


# print(data[0]['points'][0]['x'])

print(x_values, y_values)

fig1 = px.line(x=x_values,y=y_values)
fig2 = px.line(x=x_values,y=y_leak)

fig = make_subplots(rows=2, cols=1,
                    shared_xaxes=True
                    )

fig.add_trace(
    go.Line(x=x_values,y=y_values, name="Sea Level (m)"),
    row=1, col=1,
    
)
fig.add_hline(y=leak_height)
fig.add_trace(
    go.Scatter(x=x_values,y=y_leak, name="Leak Rate (L/hr)"),
    row=2, col=1,
)
# fig = go.Figure(data = fig1.data + fig2.data)
# fig.show()
fig.write_html("Plots/output.html")


print(pd.to_datetime(int(data[1]['points'][5]['x']), utc=True, unit='s'))



# Closing file
f.close()
