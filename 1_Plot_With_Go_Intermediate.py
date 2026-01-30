"""
This example demonstrates intermediate-level plotting using Plotly Graph Objects.
It shows how to create more customized plots like Scatter3D, ScatterGeo, Choropleth, and Surface plots.
"""
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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col( html.H1(children='Yeah babe!'), width=2),
        dbc.Col( dcc.Markdown(my_markdown), width=2),
        dbc.Col([html.H4("Dropdown Selection:"), html.Div(id="output", style={"border": "1px solid white", "padding": "10px", "color": "white"})], width=2),
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
            figure=go.Figure(data=go.Scatter(x=age, y=height, mode="markers"), layout=go.Layout(title="Scatter"))
        ), width=4),
        # https://plotly.com/python/reference/scatter3d/
        dbc.Col(dcc.Graph(
            id='scatter3d',
             figure=go.Figure(data=go.Scatter3d(x=age, y=height, z=weight, mode="markers"), layout=go.Layout(title="Scatter3D"))
        ), width=4),
        # https://plotly.com/python/reference/scattergeo/
        dbc.Col(dcc.Graph(
            id='scattergeo',
            figure=go.Figure(data=go.Scattergeo(lat=age, lon=height, mode="markers"), 
                             layout=go.Layout(title="ScatterGeo"))
        ), width=4),
    ]),
    # ================= First row of plots ===================
    dbc.Row([
        # https://plotly.com/python/reference/image/
        dbc.Col(dcc.Graph(
            id='imshow',
            figure=go.Figure(data=go.Image(z=255*np.random.random((200,200,3))), layout=go.Layout(title="Image (go.Image)"))
        ), width=4),

        # https://plotly.com/python/reference/surface/
        dbc.Col(dcc.Graph(
            id='surface',
            # The link between the dataframe and the countries is trough the 'locations' attribute.
            # https://plotly.com/python/reference/layout/scene/
            figure=go.Figure(data=go.Surface(z=Z), layout=go.Layout(title="Surface (go.Surface)", scene={
                'bgcolor':"rgb(250,0,0)",
                "xaxis": {"nticks": 20},
                "zaxis": {"nticks": 4},
                'camera_eye': {"x": 0, "y": -1, "z": 0.5},
                "aspectratio": {"x": 1, "y": 1, "z": 1}
            }))
), width=4),
    ]),
    # ================= Mapbox and Advanced Geo Plots ===================
    dbc.Row([
        # https://plotly.com/python/scattermapbox/
        dbc.Col(dcc.Graph(
            id='scattermapbox',
            figure=go.Figure(data=go.Scattermapbox(lat=age, lon=height, mode='markers', marker=go.scattermapbox.Marker(size=9)),
                             layout=go.Layout(title="ScatterMapbox", mapbox_style="open-street-map", mapbox_center_lat=np.mean(age), mapbox_center_lon=np.mean(height), mapbox_zoom=3))
        ), width=4),
         # https://plotly.com/python/mapbox-density-heatmaps/
        dbc.Col(dcc.Graph(
            id='densitymapbox',
            figure=go.Figure(data=go.Densitymapbox(lat=age, lon=height, z=weight, radius=10),
                             layout=go.Layout(title="DensityMapbox", mapbox_style="open-street-map", mapbox_center_lat=np.mean(age), mapbox_center_lon=np.mean(height), mapbox_zoom=3))
        ), width=4),
        # https://plotly.com/python/lines-on-maps/
        dbc.Col(dcc.Graph(
            id='linegeo',
            figure=go.Figure(data=go.Scattergeo(lat=age, lon=height, mode="lines", line=dict(width=2, color="blue")),
                             layout=go.Layout(title="LineGeo (ScatterGeo lines)"))
        ), width=4),
    ]),
    dbc.Row([
        # https://plotly.com/python/choropleth-maps/#choroplethmapbox
        dbc.Col(dcc.Graph(
            id='choroplethmapbox',
            # Using the same data as the choropleth example
            figure=go.Figure(data=go.Choroplethmapbox(z=df['unemp'], locations=df['fips'], geojson=counties, colorscale="Viridis", zmin=0, zmax=12),
                             layout=go.Layout(title="ChoroplethMapbox", mapbox_style="carto-positron", mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129}))
        ), width=12),
    ]),
    dbc.Row([
        dbc.Col(dcc.Markdown("""
### Map Figures in Dash/Plotly
Here is a comprehensive list of figures related to maps available in Dash (via Plotly):

1. **ScatterGeo** (`go.Scattergeo` / `px.scatter_geo`): Scatter plots on geographic maps. Good for points on globe/maps.
2. **Choropleth** (`go.Choropleth` / `px.choropleth`): Colored regions based on values (e.g., states, countries).
3. **ScatterMapbox** (`go.Scattermapbox` / `px.scatter_mapbox`): Scatter plots on Mapbox tiles. Allows for detailed street/satellite basemaps.
4. **ChoroplethMapbox** (`go.Choroplethmapbox` / `px.choropleth_mapbox`): Choropleth on Mapbox tiles.
5. **DensityMapbox** (`go.Densitymapbox` / `px.density_mapbox`): Density heatmaps on Mapbox tiles.
6. **LineGeo** (`px.line_geo`): Lines on geographic maps (e.g. flight paths).
7. **FilledArea** (`px.area_geo`? No, simpler `go.Scattergeo` with mode='lines' or `fill` options could mimic areas).

Mapbox figures require a Mapbox access token for some styles, but 'open-street-map' style is free.
        """), width=12)
    ])
])

# IMPORTANT READ THE OUTPUT
# print(help(dcc.Dropdown))
@app.callback(
    Output('output', 'children'),
    [Input('demo-dropdown', 'value')])
def display_relayout_data(value):
    if value is not None:
        return f"Selected: {value}"
    return "Select a city"


if __name__ == '__main__':
    app.run(debug=True)