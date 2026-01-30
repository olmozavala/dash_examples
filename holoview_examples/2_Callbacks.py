"""
This example demonstrates callback implementation in Panel using pn.bind.
It includes:
1. Basic text input callbacks (replicates '3_Callbacks.py')
2. Map callbacks with OpenStreetMap tiles - capturing hover, click, and zoom/pan events
"""
import panel as pn
import holoviews as hv
import geoviews as gv
import json
import cartopy.crs as ccrs

hv.extension('bokeh')
pn.extension()

# ============================================================================
# Section 1: Basic Callbacks with Text Inputs
# ============================================================================

# 1. Define Widgets
input1 = pn.widgets.TextInput(name='Input 1', value='initial value')
input2 = pn.widgets.TextInput(name='Input 2', value='second value')

# 2. Define Callback Functions
# In Panel, we can bind functions to widget values.

def update_output1(in1, in2):
    return f"You've entered {in1} and {in2}"

def update_output2(in2):
    return f"Second input: {in2}"

# 3. Bind functions to inputs
# pn.bind creates a reactive object that updates whenever the bound parameters change.
out1 = pn.bind(update_output1, in1=input1, in2=input2)
out2 = pn.bind(update_output2, in2=input2)

# 4. Layout for basic callbacks
basic_section = pn.Column(
    "## Basic Callbacks with Panel",
    pn.Row(input1, input2),
    pn.pane.Markdown(out1, styles={'background': '#f0f0f0', 'padding': '10px'}),
    pn.pane.Markdown(out2, styles={'background': '#e0e0e0', 'padding': '10px'})
)

# ============================================================================
# Section 2: Map Callbacks with OpenStreetMap + PolyDraw
# ============================================================================

# Create a base map with OSM tiles
# Note: Tiles do NOT support 'hover' or 'tap' tools in Bokeh, 
# but they can still be used as a source for PointerXY/Tap streams.
tiles = gv.tile_sources.OSM().opts(
    active_tools=['pan', 'wheel_zoom']
)

# Create a Points element to enable interaction
sample_points = gv.Points(
    [(-82, 27), (-85, 29), (-90, 28)],  # Sample points (lon, lat)
    crs=ccrs.PlateCarree()
).opts(
    size=12, 
    color='red',
    tools=['hover', 'tap', 'box_select', 'lasso_select'],
    hover_fill_color='orange',
    selection_color='blue'
)

# Create an empty Path element for drawing lines
# We attach the PolyDraw stream specifically to this element
draw_path = gv.Path([], crs=ccrs.PlateCarree()).opts(
    line_width=3,
    color='blue'
)

# Create the PolyDraw stream
# This adds the 'poly_draw' tool to the UI
poly_draw_stream = hv.streams.PolyDraw(
    source=draw_path, 
    drag=True,
    num_objects=5,
    show_vertices=True,
    vertex_style={'fill_color': 'white', 'size': 8}
)

# Create the map overlay
osm_map = (tiles * sample_points * draw_path).opts(
    width=600, 
    height=400,
    title="Interactive OSM Map - Draw lines with poly_draw tool",
    # Set the drawing tool as active by default
    active_tools=['poly_draw'],
    tools=['save', 'reset', 'wheel_zoom', 'pan', 'poly_draw']
)

# Define Streams to capture map events
# We source them from tiles + sample_points + draw_path (the map components)
pointer_stream = hv.streams.PointerXY(source=osm_map)
tap_stream = hv.streams.Tap(source=osm_map)
range_stream = hv.streams.RangeXY(source=osm_map)

# Create display panes for the stream data
def format_coords(x, y, label="Coordinates"):
    """Format coordinates, handling None values."""
    if x is None or y is None:
        return f"**{label}**\n\n*Move mouse over map or click*"
    return f"**{label}**\n\n- X: `{x:.2f}`\n- Y: `{y:.2f}`"

def format_range(x_range, y_range):
    """Format the viewport range."""
    if x_range is None or y_range is None:
        return "**Viewport Bounds**\n\n*Zoom or pan to see bounds*"
    return f"""**Viewport Bounds**

- X: `{x_range[0]:.0f}` to `{x_range[1]:.0f}`
- Y: `{y_range[0]:.0f}` to `{y_range[1]:.0f}`
"""

def format_poly_draw(data):
    """Format the drawn polyline data from PolyDraw stream."""
    if data is None or not data.get('xs') or len(data['xs']) == 0:
        return """**Drawn Lines (PolyDraw)**

*Click the pencil icon in the toolbar, then click on the map to draw. Double-click to finish.*
"""
    
    num_lines = len(data['xs'])
    lines_info = []
    for i, (xs, ys) in enumerate(zip(data['xs'], data['ys'])):
        num_points = len(xs) if xs else 0
        lines_info.append(f"- Line {i+1}: {num_points} points")
    
    return f"""**Drawn Lines (PolyDraw)**

Total lines: {num_lines}
{chr(10).join(lines_info)}
"""

# Bind stream parameters to display functions
hover_display = pn.bind(format_coords, x=pointer_stream.param.x, y=pointer_stream.param.y, label="Hover Position")
click_display = pn.bind(format_coords, x=tap_stream.param.x, y=tap_stream.param.y, label="Last Click Position")
range_display = pn.bind(format_range, x_range=range_stream.param.x_range, y_range=range_stream.param.y_range)
poly_draw_display = pn.bind(format_poly_draw, data=poly_draw_stream.param.data)

# Layout for map callbacks section
map_section = pn.Column(
    "## Map Callbacks with OpenStreetMap + PolyDraw",
    "**Instructions:** Use the pencil tool (poly_draw) to draw lines. **Click** to add points, **double-click** to finish.",
    osm_map,
    pn.Row(
        pn.Column(
            pn.pane.Markdown(hover_display, styles={'background': '#e3f2fd', 'padding': '10px'}),
            width=220
        ),
        pn.Column(
            pn.pane.Markdown(click_display, styles={'background': '#e8f5e9', 'padding': '10px'}),
            width=220
        ),
        pn.Column(
            pn.pane.Markdown(range_display, styles={'background': '#fff3e0', 'padding': '10px'}),
            width=220
        ),
        pn.Column(
            pn.pane.Markdown(poly_draw_display, styles={'background': '#f3e5f5', 'padding': '10px'}),
            width=220
        ),
    )
)

# ============================================================================
# Combined Layout
# ============================================================================

layout = pn.Column(
    "# Callbacks Examples with Panel and HoloViews",
    basic_section,
    pn.layout.Divider(),
    map_section
)

if __name__ == '__main__':
    # Use autoreload=True for hot reload during development
    pn.serve(layout, port=8062, autoreload=True)
