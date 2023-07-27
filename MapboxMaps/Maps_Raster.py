# %%
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import datashader.transfer_functions as tf
import colorcet as cc
from textwrap import dedent as d
import xarray as xr
import numpy as np

# https://dash.plot.ly/interactive-graphing
# https://plot.ly/python-api-reference/

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

ds = xr.open_dataset("/home/olmozavala/Dropbox/TestData/netCDF/gfs.nc", decode_times=False)
# print(ds.data_vars.values())
# %%
# # agg is an xarray object, see http://xarray.pydata.org/en/stable/ for more details
LAT = ds.lat_0.values
LON = ds.lon_0.values
# topleft, topright, bottom right, bottom left
minlon = int(np.min(LON))
maxlon = int(np.max(LON))
minlat = int(np.min(LAT))
maxlat = int(np.max(LAT))

minlon = 0
maxlon = 360
minlat = -80.0
maxlat = 80.0
# topleft, topright, bottom right, bottom left
coordinates = [[minlon, minlat], [maxlon, minlat], [maxlon, maxlat], [minlon, maxlat]]

print(f"Making transformation ....")
img = tf.shade(ds['TMP_P0_2L106_GLL0'][0,:,:], cmap=cc.rainbow)
# img = tf.Image(ds['TMP_P0_2L106_GLL0'][0,:,:])
print(f"Image properties: {img}")

print(f"Done!")
# %% Plot the img using matplotlib (for debugging)
# import matplotlib.pyplot as plt
# plt.imshow(img, origin='lower')
# plt.show()

# %%
fig = dict(
    data=[
        dict(
            lat=[0 for x in range(10)],
            lon=[x*10 for x in range(10)],
            text=['text'],
            # type="scattermapbox",
            # type="choroplethmapbox",
            type="densitymapbox",
            customdata=['custom'],
            # https://plot.ly/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
            # https://plotly.com/python/reference/#scattermapbox
            # fill="none", # none, toself, (only toself is working
            marker=dict(
                color='blue',
                fill="toself"
            ),
        )
    ],
    layout=dict(
        # https://plotly.com/python/reference/#layout-mapbox
        mapbox=dict(
            layers=[{
                "sourcetype": "image",
                "source": img.to_pil(),
                "coordinates": coordinates,
                "type": "raster",
                "below": "traces"
            }],
            center=dict(
                # lat=center[1], lon=center[0]
                lat=20, lon=0
                ),
# bearing=30, # Rotated angle
            # https://plotly.com/javascript/mapbox-layers/
            # https://plotly.com/python/reference/#layout-mapbox-style
            style='carto-positron',
            # open-street-map, white-bg, carto-positron, carto-darkmatter,
            # stamen-terrain, stamen-toner, stamen-watercolor
            pitch=0,
            zoom=0.5,
        ),
        autosize=True,
        title="Title",
        margin=dict(
            l=10, r=10, t=30, b=20
        )
    ))

the_map = dcc.Graph(figure=fig, id="id-map")

app.layout = dbc.Container(
                    [
                        dbc.Row(dbc.Col(the_map, width=12)),
                        dbc.Row([
                            dbc.Col([
                                dcc.Markdown(d("""
                                            **Hover Data**
                                            Mouse over values in the graph.
                                        """)),
                                html.P(id='hover-data')
                            ])
                        ]),
                  ])

@app.callback(
    Output('hover-data', 'children'),
    [Input('id-map', 'hoverData')])
def display_hover_data(hoverData):
    return [hoverData]
# %% 


if __name__ == '__main__':
    app.run_server(debug=True)

# %%
