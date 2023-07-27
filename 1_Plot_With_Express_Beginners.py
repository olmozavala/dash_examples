#%%
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pandas import DataFrame
import numpy as np
from data.Generate_Data_For_Examples import *

##%
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
    # ================= Using plotly express https://plotly.com/python-api-reference/plotly.express.html
    dbc.Row([
        # https://plotly.com/python-api-reference/generated/plotly.express.scatter.html#plotly.express.scatter
        dbc.Col(dcc.Graph(
            id='scatter',
            figure=px.scatter(DataFrame({"age":age, "height":height}), x="age", y="height", title="Scatter")
        ), width=4),
        # https://plotly.com/python-api-reference/generated/plotly.express.scatter_3d.html#plotly.express.scatter_3d
        dbc.Col(dcc.Graph(
            id='scatter3d',
            figure=px.scatter_3d(DataFrame({"age":age, "height":height, "weight":weight}),
                              x="age", y="height", z="weight", title="Scatter3D")
        ), width=4),
        # https://plotly.com/python-api-reference/generated/plotly.express.scatter_geo.html#plotly.express.scatter_geo
        dbc.Col(dcc.Graph(
            id='scattergeo',
            figure=px.scatter_geo(DataFrame({"lat":age, "lon":height}),
                                 lat="lat", lon="lon",  title="Scatter_Geo", projection="robinson")
        ), width=4),
    ]),
    # ================= Second row of plots ===================
    dbc.Row([
        # https://plotly.com/python-api-reference/generated/plotly.express.imshow.html#plotly.express.imshow
        dbc.Col(dcc.Graph(
            id='imshow',
            figure=px.imshow(np.random.random((200,200)))
        ), width=4),
        # https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html#plotly.express.choropleth
        dbc.Col(dcc.Graph(
            id='choromap',
            # The link between the dataframe and the countries is trough the 'locations' attribute.
            figure=px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                                 color_continuous_scale="Viridis",
                                 range_color=(0, 12),
                                 scope="usa",
                                 labels={'unemp':'unemployment rate'}
                                 )
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
    # app.run_server(debug=False, port=8051, host='146.201.212.115')