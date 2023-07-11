import json
from textwrap import dedent as d
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import xarray as xr

import pandas as pd

# https://dash.plot.ly/interactive-graphing
# https://plot.ly/python-api-reference/   (ploty API)
# https://plot.ly/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure

file_name = "/home/olmozavala/Dropbox/TestData/netCDF/GoM_Separated_U_V/022GOMl0.04-1992_002_00_u.nc"
data = xr.open_dataset(file_name)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

lats = data.Latitude.values
lons = data.Longitude.values

LONS, LATS = np.meshgrid(lons, lats)

lats_all = LATS.flatten()
lons_all = LONS.flatten()

u = data.u.values[0,0,:,:]
minu = np.nanmin(u)
maxu = np.nanmax(u)
vals = (u.flatten() - minu)/(maxu - minu)
notnan = np.logical_not(np.isnan(vals))

app.layout = html.Div([
    dcc.Graph(
        id="id-map",
        figure=dict(
            # https://plot.ly/python-api-reference/generated/plotly.graph_objects.Densitymapbox.html
            data=[
                dict(
                    # lat=np.arange(37.5, 41.5, .5),
                    # lon=np.arange(-95.5, -99.5, -.5),
                    # z=[1, .9, .8, .7, .3, .1, 0],
                    lat=lats_all[notnan],
                    lon=lons_all[notnan],
                    z=vals[notnan],
                    type="densitymapbox",
                    # scattermapbox, choroplethmapbox, densitymapbox, scattergeo
                    radius=1,
                    colorscale=[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']],
                )
            ],
            layout=dict(
                mapbox=dict(
                    layers=[],
                    center=dict(
                        lat=38.72490, lon=-95.61446
                    ),
                    style='open-street-map',
                    # open-street-map, white-bg, carto-positron, carto-darkmatter,
                    # stamen-terrain, stamen-toner, stamen-watercolor
                    pitch=0,
                    zoom=3.5,
                ),
                annotations=[dict(
                    arrowcolor='red',
                    text=' Sopas pericon ',
                    x=0.95,
                    y=0.85,
                    ax=-60,
                    ay=0,
                    arrowwidth=5,
                    arrowhead=1,
                    bgcolor="#FFFFFF",
                    font=dict(color="#2cfec1"),
                )],
                autosize=True,
            )
        )
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
