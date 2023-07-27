import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import cmocean
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pandas import DataFrame
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
    # Start here to refresh https://dash.plotly.com/dash-core-components/graph
    dbc.Row([
        # ================= Using plotly express https://plotly.com/python-api-reference/plotly.express.html
        dbc.Col(dcc.Graph(
            id='with_px',
            figure=px.scatter(DataFrame({"age":age, "height":height}), x="age", y="height", title="Express")
        ), width=4),
        # ================= Using graph objects https://plotly.com/python/reference/
        dbc.Col(dcc.Graph(
            id='with_go',
            #https://plotly.com/python/reference/layout/#layout-title
            figure=go.Figure(data=go.Scatter(x=age, y=height), layout=go.Layout(title="GO"))
        ), width=4),
        # ================= Using lists and dicts
        dbc.Col(dcc.Graph(
            id='with_lists_dicts',
            figure={
                'data': [{'x':age, 'y': height}],
                #https://plotly.com/python/reference/layout/#layout-title
                'layout': {'title':'ListsAndDics' }
            }
        ), width=4),
    ]),
    # ================= Second row of plots ===================
    dbc.Row([
        dbc.Col(dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': { #https://plotly.com/python/reference/layout/#layout-title
                    'title': 'Bars and background color',
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font':{
                        'color': colors['text']
                    }
                }
            }
        ), width=4),
        dbc.Col(dcc.Graph(
            id='lines',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2],  'name': 'line 1'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5],  'name': 'line 2'},
                ],
                'layout': { 'title': 'Simple lines', } #https://plotly.com/python/reference/layout/#layout-title
            }
        ), width=4),
        dbc.Col(dcc.Graph(
            id='scatter',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'mode':'markers', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'mode':'markers', 'name': u'Montréal'},
                ],
                'layout': { #https://plotly.com/python/reference/layout/#layout-title
                    'title': 'Scatter plot',
                }
            }
        ), width=4),
    ]),
    # ================= third row of plots ===================
    dbc.Row([
        dbc.Col(dcc.Graph(
            id='combined',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'mode': 'markers', 'name': 'line 1'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'mode':'lines', 'name': 'line 2'},
                ],
                'layout': { 'title': 'Combined plots', 'plot_bgcolor':'grey'}
            }
        ), width=4),
        dbc.Col(dcc.Graph(
            id='errorbar',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2],
                     'error_y':dict( type='percent', # value of error bar given as percentage of y value
                                            value=50,
                                            visible=True),
                     'mode':'markers', 'name': 'percentage'},
                    {'x': [1.1, 2.1, 3.1], 'y': [4, 1, 2],
                     'error_y':dict(type='data', # value of error bar given as percentage of y value
                                     array=[1, 1, .5],
                                     visible=True),
                     'mode':'markers', 'name': 'value'},
                    {'x': [1.3, 2.3, 3.3], 'y': [4, 1, 2],
                     'error_x':dict(type='data', # value of error bar given as percentage of y value
                                    array=[.1, .2, .3],
                                    visible=True),
                     'mode':'markers', 'name': 'horizontal'},
                ],
                'layout': { # https://plotly.com/python/reference/layout/#layout-title
                    'title': 'Erro bars',
                    'modebar': {'orientation': 'v'},
                    'grid':{'xaxis':['a','b','c']},
                    'xaxis':{'title':'Sopas'},
                    'yaxis':{'title':'Y Sopas'}
                }
            }
        ), width=4),
        dbc.Col(dcc.Graph(
            id='colorpalette',
            figure={
                'data': [
                    dict(x=np.arange(N),
                         y=np.arange(N),
                         mode='markers',
                         marker=dict(
                             color = colors_str
                             )
                         ),
                ],
                'layout': { #https://plotly.com/python/reference/layout/#layout-title
                    'title': 'Color palettes',
                }
            }
        ), width=4),
    ])
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
    app.run_server(debug=True, port=8051)