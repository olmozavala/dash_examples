"""
This example demonstrates how to overlay raster images on a map using HoloViz (GeoViews, Datashader, and Panel).
This version uses Panel instead of Dash, showcasing a more idiomatic HoloViz workflow.
"""
import xarray as xr
import numpy as np
import holoviews as hv
import geoviews as gv
import panel as pn
from holoviews.operation.datashader import rasterize
import cartopy.crs as ccrs

# Initialize HoloViews and Panel
hv.extension('bokeh') # Using Bokeh for Panel as it's more feature-rich for HoloViz
pn.extension()

# 1. Load Data
ds = xr.open_dataset("/home/olmozavala/Dropbox/TestData/netCDF/gfs.nc", decode_times=False)
data_slice = ds['TMP_P0_2L106_GLL0'][0,:,:]

# 2. Adjust Coordinates (0-360 to -180-180)
data_slice.coords['lon_0'] = (data_slice.coords['lon_0'] + 180) % 360 - 180
data_slice = data_slice.sortby('lon_0')

# 3. Create HoloViz Visualization
# Define the Image element
img_el = gv.Image(data_slice, kdims=['lon_0', 'lat_0'], vdims=['TMP_P0_2L106_GLL0'], crs=ccrs.PlateCarree())

# Rasterize using datashader
rasterized = rasterize(img_el).opts(
    cmap='rainbow', alpha=0.7, 
    colorbar=True, width=800, height=500,
    title="Global Temperature (GFS) - HoloViz (Panel)"
)

# Add map tiles
tiles = gv.tile_sources.OSM()
plot = (tiles * rasterized).opts(active_tools=['wheel_zoom', 'pan'], tools=['tap'])

# 4. Interactivity with Tap stream
# Panel handles HoloViews streams natively
# Assign the Tap stream to the base Image element to ensure it captures events
# even when rasterized/overlaid.
tap = hv.streams.Tap(source=img_el, x=-84, y=30) # Default starting point

# Define a function to update a text element on tap
def get_point_value(x, y):
    if x is None or y is None:
        return "## Click on the map to see details"
    try:
        # Query GFS data at tapped location
        val = data_slice.sel(lat_0=y, lon_0=x, method='nearest').values
        return f"### Clicked Location\n**Lat:** {y:.4f} | **Lon:** {x:.4f}\n\n**Temperature:** {val:.2f} K"
    except Exception as e:
        return f"Error: {e}"

# Bind the function to the tap stream
info = pn.bind(get_point_value, x=tap.param.x, y=tap.param.y)

# 5. Create Dashboard Layout
dashboard = pn.Column(
    "# GFS Temperature Map (Panel + HoloViz)",
    pn.Row(plot, pn.Card(info, header="Point Info", width=250)),
    max_width=1100
)

# Serve the app (pn.serve is used for standalone scripts)
if __name__ == '__main__':
    # You can run this with: python Maps_Raster_Holoviz_Panel.py
    # or: panel serve Maps_Raster_Holoviz_Panel.py
    pn.serve(dashboard, port=8055)
