import json
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

import pandas as pd

# https://dash.plot.ly/interactive-graphing
# https://plot.ly/python-api-reference/

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# The annotation in the upper right corner of th emap
my_anotation = dict(
    arrowcolor='red',
    text=' Sopas pericon ',
    x=0.95,
    y=0.85,
    ax=-60,
    ay=0,
    arrowwidth=5,
    arrowhead=0,
    bgcolor="#FFFFFF",
    font=dict(color="#2cfec1"),
)


# =========== The easiest way is to use scatter_mapbox from a dataframe or from data ============
# https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_mapbox.html
# https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
# fig = px.scatter_mapbox(data_frame=us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
#                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig = px.scatter_mapbox(lat=np.arange(37.5, 41.5, .5), lon=np.arange(-95.5, -99.5, -.5),
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}, annotations=[my_anotation])
the_map1 = dcc.Graph(figure=fig, id="id-map")

# =========== This option is harder, but you can manipulate multiple layers easily
lats = np.arange(37.5, 41.5, .5)
lons = np.arange(-95.5, -99.5, -.5)
my_data = [ # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
    dict( # First layer
        lat=lats,
        lon=lons,
        type="scattermapbox",
        # fill="none", # none, toself, (only toself is working
        customdata=[F"Nany:{x}" for x in lats],
        meta=[F"META:{x}" for x in lons],
        hovertemplate="This is my template lat:%{lat} lon:%{lon} custom:%{meta}",
        hoverinfo=None,
        title="Title",
        marker=dict(
            # cmin=np.amin(lons),
            # cmax=np.amax(lons),
            # autocolorscale=True,
            # color=lons,
            color=lons,
            colorscale="Greens", # Greys,YlGnB u,Greens,YlOrRd,Bluered,RdBu,Reds,Blues,Picnic,Rainbow,Portland ,Jet,Hot,Blackbody,Earth,Electric,Viridis,Cividis.
            # https://plotly.com/python/builtin-colorscales/
            # reversescale = True,
            colorbar=dict( # https://plotly.com/python-api-reference/generated/plotly.graph_objects.scattermapbox.marker.html#plotly.graph_objects.scattermapbox.marker.ColorBar
                bgcolor="white",
                title="cb title",
                xpad=100
            )
            # color=[x for x in range(len(lons))]
        )
    ),
    dict( # Second layer
        lat=np.arange(37.5, 41.5, .5),
        lon=np.arange(-95.5+1, -99.5+1, -.5),
        type="scattermapbox",
        # https://plot.ly/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
        # fill="none", # none, toself, (only toself is working
        marker=dict( color='blue' ),
    )
]
# These types of map have "style" to define the base map and data, to render above map
the_map2 = dcc.Graph(
    id="id-map2",  # id
    figure=dict(
        data= my_data,
        layout=dict(
            mapbox=dict(
                center=dict(
                    lat=38.72490, lon=-95.61446
                ),
                style='open-street-map',
                # open-street-map, white-bg, carto-positron, carto-darkmatter,
                # stamen-terrain, stamen-toner, stamen-watercolor
                pitch=0,
                zoom=3.5,
            ),
            annotations=[my_anotation],
            autosize=True,
        )
    ))

app.layout = html.Div([
    the_map1,
    the_map2,
    html.Div(children=[
        html.Div([
            dcc.Markdown(d(""" **Hover Data Map 1** """)),
            html.Pre(id='hover-data')
        ], className='three columns'),
        html.Div([
            dcc.Markdown(d(""" **Hover Data Map 2** """)),
            html.Pre(id='hover-data-2')
        ], className='three columns'),
        html.Div([
            dcc.Markdown(d("""
                **Click Data**

                Click on points in the graph.
            """)),
            html.Pre(id='click-data'),
        ], className='three columns'),

        html.Div([
            dcc.Markdown(d("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also 
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """)),
            html.Pre(id='selected-data'),
        ], className='three columns'),

        html.Div([
            dcc.Markdown(d("""
                **Zoom and Relayout Data**

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire
                this event.
            """)),
            html.Pre(id='relayout-data'),
        ], className='three columns')
    ])
])

@app.callback(
    Output('hover-data', 'children'),
    [Input('id-map', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

@app.callback(
    Output('hover-data-2', 'children'),
    [Input('id-map2', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

@app.callback(
    Output('click-data', 'children'),
    [Input('id-map', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('selected-data', 'children'),
    [Input('id-map', 'selectedData')])
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


@app.callback(
    Output('relayout-data', 'children'),
    [Input('id-map', 'relayoutData')])
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)
