# %%
import holoviews as hv
import panel as pn
from holoviews import streams

hv.extension("bokeh")
pn.extension()

# A visible background so you can tell the plot is rendered
bg = hv.Points([(0, 0), (1, 1), (2, 0), (3, 1)]).opts(
    size=8, alpha=0.4,
    width=700, height=450,
    xlim=(-1, 4), ylim=(-1, 2),
    show_grid=True,
    title="Select the poly_draw tool, then LEFT-click to add vertices, DOUBLE-click to finish"
)

# This is where drawn polylines will appear
paths = hv.Path([]).opts(line_width=3)

# Attach drawing stream
draw = streams.PolyDraw(source=paths)

# Live readout of vertices
@pn.depends(draw.param.data)
def readout(_):
    data = draw.data
    # data is typically {'xs': [[...], ...], 'ys': [[...], ...]}
    return pn.pane.JSON(data, depth=6, sizing_mode="stretch_width")

layout = pn.Row(
    pn.Column(bg * paths, sizing_mode="fixed"),
    pn.Column("### Drawn vertices (updates live)", readout, sizing_mode="stretch_width")
)

layout
# %%