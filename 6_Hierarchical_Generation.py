"""
This example demonstrates hierarchical dynamic content generation.
It shows how to create nested levels of buttons and content programmatically based on user interactions.
"""
import json
from textwrap import dedent as d

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, ctx, Input, Output, State, ALL, callback
from dash.exceptions import PreventUpdate
import numpy as np

# https://dash.plotly.com/sharing-data-between-callbacks
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# Colors available for bootstrap components in a list
color_options = [
    "primary",
    "secondary",
    "success",
    "warning",
    "danger",
    "info",
    "light",
    "dark",
]

def add_nextlevel(level, id, width):
    return dbc.Col(
        dbc.Button(
            f"level: {level} number: {id}",
            id={"type": f"level_{level}", "index": id},
            color=[color_options[id % len(color_options)]],
        ),
        width=width,
    )

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Hierarchical Generation", style={"textAlign": "center"}),
                width={"size": 6, "offset": 3},
            )
        ),
        dbc.Row(
            html.Div(
                dbc.Col(
                    dbc.Button("Add Level", id="main_button", color="secondary"),
                    width={"size": 6, "offset": 3},
                    align="center",
                ),
                style={"display": "flex", "justifyContent": "center"},
            )
        ),
        dbc.Row(
                dbc.Col([], width=12, id="display_area"))
    ],
    fluid=True,
    id="container",
)

@callback(
    Output("display_area", "children"),
    State("display_area", "children"),
    Input("main_button", "n_clicks"),
    Input({"type": "level_1", "index": ALL}, "n_clicks"),
)
def display_relayout_data(prev_children, n_clicks, lev2_n_clicks_all):
    triggered_id = ctx.triggered_id
    print(triggered_id)
    if triggered_id == None:
        print("No triggered_id")
        return []
    elif triggered_id == 'main_button':
        print(f"Main button clicked: {triggered_id} n_clicks: {n_clicks}")
        if n_clicks == None:
            return []
        else:
            # Get the first level of children. Verify how many rows (children) are in the first level
            # If there are no childrens, create a new Row. If there are childrens, add a new column
            new_col = add_nextlevel(1, n_clicks, 2)
            if len(prev_children) == 0: # Return a new column
                return [dbc.Row([new_col])]
            else:
                prev_children[0]["props"]["children"] = prev_children[0]["props"]["children"] + [new_col]
                return prev_children
    else:
        curr_level = int(triggered_id["type"].split("_")[1])
        lev2_clicks = np.array(lev2_n_clicks_all, dtype=np.float16)
        lev2_clicks[lev2_clicks == None] = np.nan
        max_lev2_clicks = np.nansum(lev2_clicks)
        new_col = add_nextlevel(curr_level+1, int(max_lev2_clicks), 2)
        if len(prev_children) <= curr_level: # In this case we don't have columns on the desired level
            return prev_children + [dbc.Row([new_col])]
        else:
            prev_children[curr_level]["props"]["children"] = prev_children[curr_level]["props"]["children"] + [new_col]
            return prev_children

if __name__ == "__main__":
    app.run(debug=True)