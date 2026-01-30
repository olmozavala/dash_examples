"""
This example demonstrates advanced plotting techniques using dictionaries for configuration.
It covers creating Heatmaps, Contours, and other complex visualizations by directly manipulating the figure dictionary structure.
"""
# %%
import dash
from urllib.request import urlopen
import json
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import cmocean
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pandas import DataFrame
import pandas as pd
import numpy as np
from data.Generate_Data_For_Examples import *
import xarray as xr
import cmocean.cm as cmo

def cmocean_to_plotly(cmap, pl_entries):
    h = 1.0/(pl_entries-1)
    pl_colorscale = []
    
    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])
        
    return pl_colorscale

thermal_rgb = cmocean_to_plotly(cmo.thermal, 255)
# print(thermal_rgb)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
ds = xr.open_mfdataset("/home/olmozavala/Dropbox/TestData/netCDF/GoM/*.nc", decode_times=False)
img_data = ds['surf_el'][0,:,:]
lats = ds['lat'].values
lons = ds['lon'].values
dx = np.mean(np.diff(lons))
dy = np.mean(np.diff(lats))

# %% Plot image with matplotib just for testing
import matplotlib.pyplot as plt
plt.imshow(img_data, origin="lower")
# plt.show()

# %%
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col( html.H1(children='Yeah babe!'), width=2),
        dbc.Col( dcc.Markdown(my_markdown), width=2),
        dbc.Col( id="output", width=2),
        dbc.Col( dcc.Dropdown(
            id='demo-dropdown',
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montreal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value='NYC'), width=2)
    ]),
    # ================= First row of plots ===================
    # ================= Using graph objects https://plotly.com/python/reference/
    dbc.Row([
        # https://plotly.com/python-api-reference/generated/plotly.express.scatter.html#plotly.express.scatter
        dbc.Col(dcc.Graph(
            id='scatter',
            figure={'data':[{'x':age, 'y':height, 'mode':"markers"}],
                    'layout':{'title': {'text': "Scatter"}, 'margin': {'t': 50}}}
        ), width=4),
        # https://plotly.com/python/reference/scatter3d/
        dbc.Col(dcc.Graph(
            id='scatter3d',
            figure={'data':[{'x':age, 'y':height, 'z':weight, 'mode':"markers", 'type':'scatter3d'}],
                    'layout':{'title': {'text': "Scatter3D"}, 'margin': {'t': 50}}}
        ), width=4),
        # https://plotly.com/python/reference/scattergeo/
        dbc.Col(dcc.Graph(
            id='scattergeo',
            figure={'data':[{'lat':age, 'lon':height, 'mode':"markers", 'type':'scattergeo'}],
                    'layout':{'title': {'text': "ScatterGeo"}, 'margin': {'t': 50}}}
        ), width=4),
    ]),
    # ================= Second row of plots ===================
    dbc.Row([
        # https://plotly.com/python/reference/heatmap/
        dbc.Col(dcc.Graph(
            id='heatmap',
            figure={'data':[ dict(
                    z=img_data.values,
                    type='heatmap', # type='heatmap' | 'heatmapgl'
                    x=lons, y=lats,
                    text="sopas",
                    hoverinfo="${z:0.2f}", # x,y,z,text,name
                    colorscale=thermal_rgb
                    )], 
                    'layout': {
                        'title': {'text': "Heatmap"},
                        'margin': {'t': 50},
                        'yaxis': {'scaleanchor': "x", 'scaleratio': 1},
                        'dragmode': "drawline",
                        # "zoom" | "pan" | "select" | "lasso" | 
                        # "drawclosedpath" | "drawopenpath" | "drawline" 
                        # "drawrect" | "drawcircle" | "orbit" | "turntable" | 
                        # All the otpions are here: https://github.com/plotly/plotly.js/blob/master/src/components/modebar/buttons.js
                    }},
            # https://plotly.com/javascript/configuration-options
            config=dict(
                modeBarButtonsToRemove=['zoom2d','zoomOut2d','zoomIn2d'],
                modeBarButtonsToAdd=['drawline', 'drawcircle', 'lasso2d', 'select2d'],
                scrollZoom=True,
                displayModeBar= True,
                displaylogo=False,
            )),
                      width=6),
        # https://plotly.com/python/reference/image/
        # dbc.Col(dcc.Graph(
        #     id='imshow',
        #     figure={'data':[{'z':img_data.data, 'type':'image'}],
        #             'layout':{'title':"Image"}}), width=6),
        # https://plotly.com/python/reference/contour/ 
        dbc.Col(dcc.Graph(
            id='imcontour',
            figure={'data':[ dict(
                    z=img_data.values,
                    type='contour',
                    x=lons, y=lats,
                    colorscale=thermal_rgb
                    )], 
                    'layout': {
                        'title': {'text': "Contour"},
                        'margin': {'t': 50},
                        'yaxis': {'scaleanchor': "x", 'scaleratio': 1},
                        'dragmode': "drawcircle",
                    }}),
                      width=6),
    ]),
    # ================= Third row Just outputs of callbacks ======
    dbc.Row([
        # https://plotly.com/python/reference/heatmap/
        dbc.Col(html.Div("Sopas", id='heatmap-output'), width=6)
        ]),
    # ================= Third row of plots ===================
    dbc.Row([
        # https://plotly.com/python/reference/choropleth/
        dbc.Col(dcc.Graph(
            id='choromap',
            # The link between the dataframe and the countries is trough the 'locations' attribute.
            figure={'data':[{'z':df['unemp'], 'zmin':0, 'zmax':12, 'locations':df['fips'],
                       'geojson':counties, 'colorscale':'Viridis', 'type':'choropleth'}],
                        'layout':{'title': {'text': "Choropleth"}, 'margin': {'t': 50}}}
        ), width=4),
        # https://plotly.com/python/reference/surface/
        dbc.Col(dcc.Graph(
            id='surface',
            # The link between the dataframe and the countries is trough the 'locations' attribute.
            # https://plotly.com/python/reference/layout/scene/
            figure={'data':[{'z':Z, 'type':'surface'}],
                'layout':{
                    'title': {'text': "Surface"},
                    'margin': {'t': 50},
                    'scene':{
                        'bgcolor':"rgb(250,0,0)",
                        "xaxis": {"nticks": 20},
                        "zaxis": {"nticks": 4},
                        'camera_eye': {"x": 0, "y": -1, "z": 0.5},
                        "aspectratio": {"x": 1, "y": 1, "z": 1}
                        }
                }}
        ), width=4),
    ]),
])

# IMPORTANT READ THE OUTPUT
# print(help(dcc.Dropdown))
@app.callback(
    Output('output', 'children'),
    [Input('demo-dropdown', 'value')])
def display_relayout_data(value):
    if value != None:
        return value

@app.callback(
    Output('heatmap-output', 'children'),
    [Input('heatmap', 'clickData'),
    Input('heatmap', 'selectedData'),
    Input('heatmap', 'relayoutData'),
     ])
def display_click_data(click_data, selected_data, relayout_data):
    print(f"Clicked data: {click_data}")
    print(f"Selected data: {selected_data}")
    print(f"Relayout data: {relayout_data}")
    return "Venga"


if __name__ == '__main__':
    app.run(debug=True, port=8051)
