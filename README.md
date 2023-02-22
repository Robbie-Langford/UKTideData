# UKTideData
## An example of how tidal data can be processed to provide useful data for engineers.
In this instance, a duct seal is positioned between low tide and high tide. This duct seal is imperfect, which results in a water leak rate that varies linearly with hydrostatic pressure. A graph was produced to plot the leak rate and daily leak volume for a whole year.

![](/Plots/output_image.png)

The graphs were generated using the plotly python library, which can output an interactive html graph.
___
Tidal data was sourced from www.willyweather.co.uk
Example json URL:
https://www.willyweather.co.uk/graphs/data.json?startDate=2022-11-5&days=100&graph=outlook:5,location:243516,series=order:0,id:sunrisesunset,type:forecast,series=order:1,id:tides,type:forecast