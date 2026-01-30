"""
This example demonstrates dynamic layout generation in Panel.
It replicates '5_DynamicGeneration.py', where clicking a button adds a new column to the layout.
"""
import panel as pn
import holoviews as hv
import numpy as np

pn.extension()

# 1. Target Container (using pn.Row as the output container)
container = pn.Row()

# 2. Function to create a new component
def create_new_column(n):
    # Creating a simple scatter plot for each new column
    return hv.Scatter(np.random.rand(10, 2)).opts(
        title=f"Col {n}", width=250, height=250,
        active_tools=['pan', 'wheel_zoom'], tools=['hover', 'save', 'reset']
    )

# 3. Callback for the button
# We use pn.widgets.Button and an on_click handler
button = pn.widgets.Button(name="Add new Row", button_type="primary")

def add_row_callback(event):
    # Calculate current count to determine width
    # In Panel, we can just append. Responsive width is handled differently.
    # We can set the width of all existing children and the new one.
    count = len(container) + 1
    width = int(800 / count) # Just an example width distribution
    
    # Add new column
    container.append(create_new_column(button.clicks))
    
    # Update widths for all columns to distribute evenly
    for child in container:
        child.width = width

button.on_click(add_row_callback)

# 4. Layout
layout = pn.Column(
    "# Dynamic Component Generation with Panel",
    button,
    container
)

if __name__ == '__main__':
    pn.serve(layout, port=8066)
