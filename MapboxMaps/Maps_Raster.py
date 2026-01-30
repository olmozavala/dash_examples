"""
This example demonstrates how to overlay raster images on a Mapbox map.
It uses Datashader to shade xarray data and projects it as an image layer on the map.
"""
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
from pyproj import Transformer

print(f"Making transformation ....")
# Reproject to Web Mercator (EPSG:3857)
# 1. Define transformers
to_mercator = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
to_latlon = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

# 2. Define grid in Web Mercator (meters)
# Mapbox Web Mercator bounds
mercator_min = -20037508.34
mercator_max = 20037508.34
# Create a grid (e.g., 1000x1000 resolution)
x = np.linspace(mercator_min, mercator_max, 2000)
y = np.linspace(mercator_min, mercator_max, 2000)
xv, yv = np.meshgrid(x, y)

# 3. Transform Web Mercator grid points back to Lat/Lon
lon_grid, lat_grid = to_latlon.transform(xv, yv)

# 4. Interpolate original data at these Lat/Lon points
# We need to construct an xarray DataArray for the target coordinates to use .interp() efficiently
# Or we can pass the 2D arrays directly if dimensions match known logic, but xarray likes specific coords.
# A simpler way with xarray is to verify the input data is sorted and distinct.
# ds is already sorted by lon_0 from previous steps if we kept that? 
# No, we reverted. So we might need to handle the 0-360 vs -180-180 for interpolation continuity.
# GFS is 0-360. Our target lon_grid is -180 to 180.
# The .interp method naturally handles out-of-bounds with NaNs unless we handle wrapping.
# To handle wrapping correctly, we should align the source data to -180..180 or append 360.
# Let's adjust source to -180..180 for safer interpolation with typical map libraries.
data_slice = ds['TMP_P0_2L106_GLL0'][0,:,:]
# Adjust data longitude to -180 to 180 for interpolation lookup
data_slice.coords['lon_0'] = (data_slice.coords['lon_0'] + 180) % 360 - 180
data_slice = data_slice.sortby('lon_0')

# Create xarray DataArrays for the new grid coordinates
# We can't pass 2D arrays directly to lat_0/lon_0 in interp like this easily if they aren't rectilinear.
# But lat/lon grid IS regular in Mercator, NOT in Lat/Lon.
# So we pass the 2D arrays as 'new coordinates'.
target_lat = xr.DataArray(lat_grid, dims=("y", "x"))
target_lon = xr.DataArray(lon_grid, dims=("y", "x"))

ds_reprojected = data_slice.interp(lat_0=target_lat, lon_0=target_lon)

img = tf.shade(ds_reprojected, cmap=cc.rainbow)
print(f"Image properties: {img}")

# 5. Define coordinates for the image layer
# These must be the Lat/Lon corners of the image.
# Since our image corresponds to the full Web Mercator world (-20037508.34 to 20037508.34),
# The corners are approx (-180, 85.0511) to (180, -85.0511)
# Note: Web Mercator cuts off at ~85.05 degrees lat.
max_lat_merc = 85.051129
coordinates = [[-180, max_lat_merc], [180, max_lat_merc], [180, -max_lat_merc], [-180, -max_lat_merc]]

print(f"Done!")

# Create a subsampled grid for interactivity (invisible points to capture clicks)
# Original grid is 2000x2000 which is 4M points (too many for scattermapbox)
# Subsample by taking every 20th point (100x100 = 10k points) or 40th (50x50 = 2.5k)
# 4M points is heavy for browser. 
# Let's try 50x50 grid for interaction.
step = 40 
lat_flat = lat_grid[::step, ::step].flatten()
lon_flat = lon_grid[::step, ::step].flatten()

# %%
fig = dict(
    # data=[
    #     # This is a scatter plot
    #     dict(
    #         lat=[0 for x in range(10)],
    #         lon=[x*10 for x in range(10)],
    #         text=['text'],
    #         # type="scattermapbox",
    #         # type="choroplethmapbox",
    #         type="densitymapbox",
    #         customdata=['custom'],
    #         # https://plot.ly/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
    #         # https://plotly.com/python/reference/#scattermapbox
    #         # fill="none", # none, toself, (only toself is working
    #         marker=dict(opacity=0.5, # Visible for debugging            
    #             color='blue',
    #             fill="toself"
    #         ),
    #     )
    # ],
    data=[dict(
        type="scattermapbox",
        lat=lat_flat,
        lon=lon_flat,
        mode='markers',
        marker=dict(opacity=0.5), # Visible for debugging
        hoverinfo='none'
    )],
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
                lat=0, lon=0
                # lat=20, lon=0
                ),
# bearing=30, # Rotated angle
            # https://plotly.com/javascript/mapbox-layers/
            # https://plotly.com/python/reference/#layout-mapbox-style
            # https://plotly.com/javascript/tile-map-layers/
            style='open-street-map',
            # open-street-map, white-bg, carto-positron, carto-darkmatter,
            # stamen-terrain, stamen-toner, stamen-watercolor, white-bg
            # basic, streets, outdoors, satellite, light, dark, satellite-streets
            pitch=0,
            zoom=1,
        ),
        autosize=True,
        title={'text': "Global Temperature (GFS)", 'x':0.5, 'y':0.95, 'xanchor': 'center', 'yanchor': 'top'},
        margin=dict(
            l=10, r=10, t=50, b=20
        )
    ))

the_map = dcc.Graph(figure=fig, id="id-map", config={'scrollZoom': True})

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
    [Input('id-map', 'clickData')])
def display_click_data(clickData):
    if clickData is None:
        return "Click on the map to see value"
    
    # Extract lat/lon from click data
    pt = clickData['points'][0]
    lat = pt['lat']
    lon = pt['lon']
    
    # Transform to Web Mercator to find logical index in our grid
    mx, my = to_mercator.transform(lat, lon)
    
    # Calculate indices
    # We used 2000 points from mercator_min to mercator_max
    # x = np.linspace(mercator_min, mercator_max, 2000)
    # index = (value - min) / (max - min) * (N - 1)
    
    # Grid parameters used in generation
    N = 2000
    # global mercator_min, mercator_max # defined in main scope
    
    ix = int((mx - mercator_min) / (mercator_max - mercator_min) * (N - 1))
    iy = int((my - mercator_min) / (mercator_max - mercator_min) * (N - 1))
    
    # Boundary checks
    if 0 <= ix < N and 0 <= iy < N:
        # ds_reprojected has dims (y, x)
        val = ds_reprojected.isel(y=iy, x=ix).values
        return f"Clicked Location: {lat:.4f}, {lon:.4f} | Temperature: {val:.2f} K"
    else:
        return f"Clicked Location: {lat:.4f}, {lon:.4f} | Value: Out of bounds"
if __name__ == '__main__':
    app.run(debug=True, port=8053)