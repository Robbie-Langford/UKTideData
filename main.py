# Python program to read cleaned json file and process data
import json

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from scipy.interpolate import InterpolatedUnivariateSpline


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
y_leak = []

x_daily_leak = []
y_daily_leak = []

for j in range(0,365):
    t_values = []
    y_temp = []
    for i in data[j]['points']:
        x_values.append(pd.to_datetime((i['x']), utc=True, unit='s'))
        y_values.append(i['y'])
        
        t_values.append(i['x'])
        if i['y'] > 4.5:
            y_leak.append(0.375*(i['y']-leak_height))
            y_temp.append(0.375*(i['y']-leak_height))
        else:
            y_leak.append(0)
            y_temp.append(0)
    integ = InterpolatedUnivariateSpline(t_values, y_temp, k=1)
    y_daily_leak.append((integ.integral(t_values[0], t_values[-1])/3600))
    x_daily_leak.append(pd.to_datetime((t_values[-1]), utc=True, unit='s'))



# print(data[0]['points'][0]['x'])

# integ = InterpolatedUnivariateSpline(t_values, y_leak, k=1)
# print(t_values)
# print(integ.integral(t_values[0], t_values[-1])/3600)

fig1 = px.line(x=x_values,y=y_values)
fig2 = px.line(x=x_values,y=y_leak)
fig3 = px.bar(x=x_daily_leak, y=y_daily_leak)

fig = make_subplots(rows=3, cols=1,
                    shared_xaxes=True
                    )

fig.add_trace(
    go.Line(x=x_values,y=y_values, name="Sea Level (m)"),
    row=1, col=1,   
)
fig.add_hline(y=leak_height, line_dash="dot", fillcolor='red', annotation_text="Duct Height")
fig.add_hline(y=7.6, annotation_text="HAT")
fig.add_hline(y=0.2, annotation_text="LAT")

fig.add_trace(
    go.Scatter(x=x_values,y=y_leak, name="Leak Rate (L/hr)"),
    row=2, col=1,
)

fig.add_trace(
    go.Bar(x=x_daily_leak, y=y_daily_leak, name="Daily Leak Volume (L)"),
    row=3, col=1,
)
# fig = go.Figure(data = fig1.data + fig2.data)
# fig.show()
fig.write_html("Plots/output.html")


print(pd.to_datetime(int(data[1]['points'][5]['x']), utc=True, unit='s'))



# Closing file
f.close()
