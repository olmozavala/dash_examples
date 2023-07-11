import json
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np
import xarray as xr

import pandas as pd


## Reading the data
file_name = "/home/olmozavala/Dropbox/TestData/netCDF/GoM_Separated_U_V/022GOMl0.04-1992_002_00_u.nc"
data = xr.open_dataset(file_name)

lats = data.Latitude.values
lons = data.Longitude.values

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

## Select the map type and the data
# https://plotly.com/python/map-configuration/
# Many properties at: https://plotly.com/python/reference/layout/geo/

# READ!!!!!! --> If you want to know all the possible attributes just add one, produce an error and look at the log (it will show you all the available properties)

# fig = go.Figure(go.Scattergeo())  # or px.scatter_geo, px_.line_geo or px.choropleth
fig = px.line_geo(lat=[0,15,20,35], lon=[5,10,25,30])  # or px.scatter_geo, px_.line_geo or px.choropleth

## Example in how to add stuff into the map
fig.update_geos(
    visible=False,  # Hides the background map
    resolution=50,   # Resolution (smaller resolution has more detail)
    ## ======= Position of map
    # center=dict(lon=0, lat=0),
    # projection_rotation=dict(lon=30, lat=30, roll=30),
    # lataxis_range=[-80,80], lonaxis_range=[-180,180],
    scope="north america",  # The available scopes are: 'world', 'usa', 'europe', 'asia', 'africa', 'north america', 'south america'.
    ## ======= Features
    showcoastlines=True, coastlinecolor="grey",
    showland=True, landcolor="LightGrey",
    showocean=True, oceancolor="LightBlue",
    showlakes=True, lakecolor="Blue",
    # projection_type="orthographic",  # 'equirectangular', 'mercator', 'orthographic', 'natural earth', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area', 'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff' and 'sinusoidal'.
    # showrivers=True, rivercolor="Blue",
    showcountries=True, countrycolor="black"
)


app.layout = html.Div([
    dcc.Graph(figure=fig, id="id_map"),
    html.Div(["sopas", html.Pre(id='output-div')], id="id_div")
])

# I HAVEN'T BEEN ABLE TO ADD EVENTS TO THIS TYPES OF MAPS, IT MAY NOT BE POSSIBLE
@app.callback(
    Output('output-div', 'children'),
    [Input('id_map', 'clickData')])
def display_hover_data(clickedData):
    print("Clicked")
    return F"Clicked {clickedData}"

#
# @app.callback(
#     Output('click-data', 'children'),
#     [Input('id-map', 'clickData')])
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)
#
#
# @app.callback(
#     Output('selected-data', 'children'),
#     [Input('id-map', 'selectedData')])
# def display_selected_data(selectedData):
#     return json.dumps(selectedData, indent=2)
#
#
# @app.callback(
#     Output('relayout-data', 'children'),
#     [Input('id-map', 'relayoutData')])
# def display_relayout_data(relayoutData):
#     return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)
