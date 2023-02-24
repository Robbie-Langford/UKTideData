#%% Python program to read cleaned json file and process data
import json

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from scipy.interpolate import InterpolatedUnivariateSpline


# Load the JSON data from file
with open('Data/data_hutton_cleaned.json') as f:
    data_in = json.load(f)

# data is a dictionary containing all points for 400 days.
# The data for each day is stored in its own list called points.
data = data_in['tides']['dataConfig']['series']['groups']

# Closing file
f.close()

LEAK_HEIGHT = 5.1

SCALE = 1.0

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
        y_values.append(i['y']*SCALE)
        
        t_values.append(i['x'])
        if (i['y']*SCALE) > LEAK_HEIGHT:
            y_leak.append(0.245*((i['y']*SCALE)-LEAK_HEIGHT))
            y_temp.append(0.245*((i['y']*SCALE)-LEAK_HEIGHT))
        else:
            y_leak.append(0)
            y_temp.append(0)
    
    # Integrate to find daily leak volume          
    integ = InterpolatedUnivariateSpline(t_values, y_temp, k=1)
    y_daily_leak.append((integ.integral(t_values[0], t_values[-1])/3600))
    x_daily_leak.append(pd.to_datetime((t_values[-1]), utc=True, unit='s'))

print("Data Processed")

#%% Plot graphs

fig = make_subplots(rows=3, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.01
                    )

fig.add_trace(
    go.Line(x=x_values, y=y_values, name="Sea Level (m)"),
    row=1, col=1)

fig.add_hline(y=LEAK_HEIGHT, line_dash="dot", fillcolor='red', annotation_text="Duct Height")
fig.add_hline(y=7.3, annotation_text="HAT")
fig.add_hline(y=0, annotation_text="LAT")

fig.add_trace(
    go.Scatter(x=x_values,y=y_leak, name="Leak Rate (L/hr)"),
    row=2, col=1)

fig.add_trace(
    go.Bar(x=x_daily_leak, y=y_daily_leak, name="Daily Leak Volume (L)"),
    row=3, col=1)

# Write figure to html file
fig.write_html("Plots/output.html")

print("Graph Generated")


#%% Generate Data Frame and output to csv
 
df = pd.DataFrame(list(zip(x_values, y_values, y_leak, y_daily_leak)),
               columns =['Time', 'Height(m)', "Leak Rate (L/hr)", "Daily Leak Volume (L)"])

df.to_csv('Data/tides.csv', encoding='utf-8', index=False)    

print("Data saved to csv")