"""
This example demonstrates dynamic layout generation.
It allows users to add new rows/columns dynamically to the application layout using callbacks.
"""
import json
from textwrap import dedent as d

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

# https://dash.plotly.com/sharing-data-between-callbacks
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def addRow(id_txt, width):
    return dbc.Col(F"New Col {id_txt}", width=width, id=F"col{id_txt}")

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(dbc.Button("Add new Row", id="button"), width=6) ),
        dbc.Row(id="output_row")
    ], id="container"
)

@app.callback(
    Output('output_row', 'children'),
    State('output_row', 'children'),
    Input('button', 'n_clicks'))
def display_relayout_data(children, clicks):
    if children == None:
        return [addRow(clicks, 12)]
    else:
        # Depending on the number of children (columns) we modify the width of the columns 
        c_width = int(12/(len(children) + 1))
        print(f"The current width in columns is {c_width}")
        for c_child in children:
            c_child["props"]["width"] = c_width
        children.append(addRow(clicks, c_width))
        return children

if __name__ == '__main__':
    app.run(debug=True)