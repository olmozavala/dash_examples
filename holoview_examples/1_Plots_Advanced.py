"""
This example demonstrates advanced plotting techniques using HoloViews and Panel.
It replicates the functionality of '1_Plots_With_Dics_Advanced.py', showing Scatter, Image, Contour, and Surface plots.
"""
import holoviews as hv
import geoviews as gv
import panel as pn
import xarray as xr
import numpy as np
import pandas as pd
import sys
import os
import cartopy.crs as ccrs
from holoviews.operation.datashader import rasterize
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.Generate_Data_For_Examples import *
# Initialize HoloViews with Bokeh (standard)
hv.extension('bokeh')
pn.extension()

# Set higher tolerance for Image sampling to avoid warnings with slightly irregular grids
hv.config.image_rtol = 0.01

# 1. Load NetCDF data
try:
    ds = xr.open_mfdataset("/home/olmozavala/Dropbox/TestData/netCDF/GoM/*.nc", decode_times=False)
    img_data = ds['surf_el'][0,:,:]
except Exception as e:
    print(f"Warning: Could not load data: {e}")
    # Fallback to dummy data
    img_data = xr.DataArray(np.random.rand(100, 100), 
                             coords={'lat': np.linspace(18, 30, 100), 'lon': np.linspace(-98, -80, 100)}, 
                             dims=('lat', 'lon'), name='surf_el')

# 2. Create Elements

# ============================  Scatter plot
scatter = hv.Scatter((age, height)).opts(
    title="Scatter", size=10, width=400, height=400,
    active_tools=['pan', 'wheel_zoom'], tools=['hover', 'save', 'reset']
)

# ============================ Scatter 2D representation of 3D data (Colored by weight)
scatter2d_rep = hv.Scatter((age, height, weight), vdims='weight').opts(
    title="Scatter (Colored by Weight)", size=10, color='weight', cmap='viridis', 
    colorbar=True, width=450, height=400,
    active_tools=['pan', 'wheel_zoom'], tools=['hover', 'save', 'reset'],
    shared_axes=False
)

# ============================ Heatmap (Image works better for hover with regular-ish grids)
heatmap = gv.Image(img_data, kdims=['lon', 'lat']).opts(
    title="Heatmap (Image)", cmap='viridis', colorbar=True, 
    width=500, height=400, active_tools=['pan', 'wheel_zoom'], 
    tools=['hover', 'save', 'reset'],
    shared_axes=False
)

# ============================ Contour
contour = hv.operation.contours(heatmap, levels=10).opts(
    title="Contour", cmap='viridis', width=500, height=400, colorbar=True,
    active_tools=['pan', 'wheel_zoom'], tools=['hover', 'save', 'reset'],
    shared_axes=False # <--- Disable axis syncing
)

# ============================ Surface representation (Heatmap)
surface_rep = hv.Image((x, x, Z)).opts(
    title="Surface (represented as Heatmap)", width=500, height=400, cmap='fire', colorbar=True,
    active_tools=['pan', 'wheel_zoom'], tools=['hover', 'save', 'reset'],
    shared_axes=False # <--- Disable axis syncing
)

# 3. Rasterization with Datashader and Geoviews Tiles
# Base geoviews image
gv_img = gv.Image(img_data, kdims=['lon', 'lat'], crs=ccrs.PlateCarree())

# Apply rasterization for large datasets (works with any size)
rasterized = rasterize(gv_img).opts(
    title="Rasterized Map with Tiles",
    cmap='viridis',
    tools=['hover'],
    colorbar=True,
    width=500, height=400,
    shared_axes=False
)

# Add background tiles
tiles = gv.tile_sources.OSM()
rasterized_map = (tiles * rasterized).opts(
    active_tools=['wheel_zoom', 'pan'],
    width=500, height=400
)

# 4. Animation Example
# We use Panel's Player widget for full playback controls (play, pause, etc.)
phases = np.linspace(0, 2 * np.pi, 21)

# Create the Player widget
player = pn.widgets.Player(
    name='Phase Player', 
    start=0, end=len(phases) - 1, value=0, 
    loop_policy='loop', interval=500, # interval in ms
    width=500
)

# Use DynamicMap to update the data WITHOUT re-creating the plot object.
# This prevents the page from scrolling/jumping on every update.
def get_anim_plot(value):
    p = phases[value]
    return hv.Image((x, x, np.cos(X + p) + np.cos(Y + p))).opts(
        title=f"Animation (Phase: {p:.2f})", 
        width=500, height=400, cmap='viridis', colorbar=True,
        active_tools=['pan', 'wheel_zoom'], tools=['hover'], 
        shared_axes=False
    )

# Link the player to the DynamicMap via streams
dmap = hv.DynamicMap(get_anim_plot, streams=[player.param.value])

# Combine plot and player into a Column with a fixed height to avoid layout shifts
# Added width to resolve Bokeh WARNING: W-1005 (FIXED_SIZING_MODE)
animation = pn.Column(dmap, player, sizing_mode='fixed', height=500, width=510)

# 5. Rasterized Map Animation
# To avoid the "Nesting a DynamicMap inside a DynamicMap" error, 
# we return a rasterized image with dynamic=False from the callback.
def get_map_data(value):
    p = phases[value]
    lons_syn = np.linspace(-100, -80, 100)
    lats_syn = np.linspace(15, 35, 100)
    LON, LAT = np.meshgrid(lons_syn, lats_syn)
    data = np.sin(LON/2 + p) * np.cos(LAT/2 + p)
    
    img = gv.Image((lons_syn, lats_syn, data), crs=ccrs.PlateCarree())
    # Rasterizing here with dynamic=False returns a static Image/QuadMesh element
    return rasterize(img, dynamic=False).opts(
        cmap='viridis', colorbar=True, width=500, height=400,
        tools=['hover'], shared_axes=False
    )

# Create the DynamicMap of rasterized results
rasterized_anim = hv.DynamicMap(get_map_data, streams=[player.param.value])

# Overlay with tiles
rasterized_anim_map = (tiles * rasterized_anim).opts(
    active_tools=['wheel_zoom', 'pan'],
    width=500, height=400
)

# 6. Layout with Panel (3 figures per row)
layout = pn.Column(
    "# Advanced Plots with HoloViews (Bokeh Backend)",
    pn.Row(scatter, scatter2d_rep, heatmap),
    pn.Row(contour, surface_rep, animation),
    pn.Row(rasterized_map, rasterized_anim_map)
)

if __name__ == '__main__':
    pn.serve(layout, port=8065)
