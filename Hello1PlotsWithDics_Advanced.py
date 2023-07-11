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
from Generate_Data_For_Examples import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
                    'layout':{'title':"Scatter"}}
        ), width=4),
        # https://plotly.com/python/reference/scatter3d/
        dbc.Col(dcc.Graph(
            id='scatter3d',
            figure={'data':[{'x':age, 'y':height, 'z':weight, 'mode':"markers", 'type':'scatter3d'}],
                    'layout':{'title':"Scatter3D"}}
        ), width=4),
        # https://plotly.com/python/reference/scattergeo/
        dbc.Col(dcc.Graph(
            id='scattergeo',
            figure={'data':[{'lat':age, 'lon':height, 'mode':"markers", 'type':'scattergeo'}],
                    'layout':{'title':"ScatterGeo"}}
        ), width=4),
    ]),
    dbc.Row([
        # https://plotly.com/python/reference/image/
        dbc.Col(dcc.Graph(
            id='imshow',
            figure={'data':[{'z':255*np.random.random((200,200,3)), 'type':'image'}],
                    'layout':{'title':"Image"}}
), width=4),
        # https://plotly.com/python/reference/choropleth/
        dbc.Col(dcc.Graph(
            id='choromap',
            # The link between the dataframe and the countries is trough the 'locations' attribute.
            figure={'data':[{'z':df['unemp'], 'zmin':0, 'zmax':12, 'locations':df['fips'],
                       'geojson':counties, 'colorscale':'Viridis', 'type':'choropleth'}],
                        'layout':{'title':"Image"}}
        ), width=4),
        # https://plotly.com/python/reference/surface/
        dbc.Col(dcc.Graph(
            id='surface',
            # The link between the dataframe and the countries is trough the 'locations' attribute.
            # https://plotly.com/python/reference/layout/scene/
            figure={'data':[{'z':Z, 'type':'surface'}],
                'layout':{
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


if __name__ == '__main__':
    app.run_server(debug=True)
