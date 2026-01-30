"""
This example shows how to handle interactive graph events using HoloViews Streams.
It replicates '4_Interactive_Callbacks.py', capturing Hover (Pointer), Tap (Click), Selection, and Range (Zoom) data.
"""
import holoviews as hv
import panel as pn
import numpy as np
import json

hv.extension('bokeh')
pn.extension()

# 1. Create a plot to interact with
# data1: x=[1, 2, 3, 4], y=[4, 1, 3, 5]
# data2: x=[1, 2, 3, 4], y=[9, 4, 1, 4]
scatter1 = hv.Scatter(([1, 2, 3, 4], [4, 1, 3, 5]), label='Trace 1').opts(size=12)
scatter2 = hv.Scatter(([1, 2, 3, 4], [9, 4, 1, 4]), label='Trace 2').opts(size=12)
overlay = (scatter1 * scatter2).opts(
    width=600, height=400, title="Interactive Graph", 
    tools=['hover', 'tap', 'box_select', 'lasso_select'],
    active_tools=['pan', 'wheel_zoom', 'box_select']
)

# 2. Define Streams to capture events
range_stream = hv.streams.RangeXY(source=overlay)
tap_stream = hv.streams.Tap(source=overlay)
pointer_stream = hv.streams.PointerXY(source=overlay)

# Selection streams (one for each trace)
selection_stream1 = hv.streams.Selection1D(source=scatter1) 
selection_stream2 = hv.streams.Selection1D(source=scatter2) 

# 3. Create display panes for the data
def format_stream_data(name, **kwargs):
    filtered = {k: v for k, v in kwargs.items() if v is not None}
    return f"**{name}**\n```json\n{json.dumps(filtered, indent=2)}\n```"

hover_pane = pn.bind(format_stream_data, "Hover Data (PointerXY)", x=pointer_stream.param.x, y=pointer_stream.param.y)
click_pane = pn.bind(format_stream_data, "Click Data (Tap)", x=tap_stream.param.x, y=tap_stream.param.y)

# Unified selection display
def format_selection(idx1, idx2):
    return f"**Selection Data**\n- Trace 1: {idx1}\n- Trace 2: {idx2}"

selection_pane = pn.bind(format_selection, idx1=selection_stream1.param.index, idx2=selection_stream2.param.index)

zoom_pane = pn.bind(format_stream_data, "Zoom/Pan Data (RangeXY)", x_range=range_stream.param.x_range, y_range=range_stream.param.y_range)

# 4. Layout
layout = pn.Column(
    "# Interactive Graph Events with HoloViews Streams",
    overlay,
    pn.Row(
        pn.Column(pn.pane.Markdown(hover_pane), width=250),
        pn.Column(pn.pane.Markdown(click_pane), width=250),
        pn.Column(pn.pane.Markdown(selection_pane), width=250),
        pn.Column(pn.pane.Markdown(zoom_pane), width=250),
    )
)

if __name__ == '__main__':
    pn.serve(layout, port=8063)
