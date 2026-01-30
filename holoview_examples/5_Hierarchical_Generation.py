"""
This example demonstrates hierarchical dynamic content generation in Panel.
It replicates '6_Hierarchical_Generation.py', where clicking buttons at one level
generates new buttons at the next level down.
"""
import panel as pn
import numpy as np

pn.extension()

# Colors for the buttons (using only Bokeh/Panel valid button_type options)
color_options = ["primary", "success", "warning", "danger", "light", "default"]

# Main container to hold rows of buttons (one row per level)
display_area = pn.Column(sizing_mode='stretch_width')

def create_button(level, count):
    """Creates a new button for a specific level."""
    # Map color options
    color = color_options[count % len(color_options)]
    
    # In Panel, 'light' and 'dark' are valid but might look different depending on theme
    # We'll use the button_type that matches the color names
    btn = pn.widgets.Button(
        name=f"level: {level} number: {count}",
        button_type=color if color not in ['light', 'dark'] else 'default',
        width=150
    )
    
    # Callback for when this button is clicked
    def on_click(event):
        add_level_content(level + 1)
        
    btn.on_click(on_click)
    return btn

def add_level_content(level):
    """Ensures a row exists for the given level and adds a new button to it."""
    # Ensure display_area has enough rows (children)
    # level 1 -> index 0, level 2 -> index 1, etc.
    while len(display_area) < level:
        new_row = pn.Row(sizing_mode='stretch_width', margin=(10, 0))
        display_area.append(new_row)
    
    target_row = display_area[level - 1]
    
    # Current button count in this row
    btn_count = len(target_row) + 1
    target_row.append(create_button(level, btn_count))

# Main Add Level button
main_button = pn.widgets.Button(name="Add Level 1", button_type="primary", width=200, align='center')
main_button.on_click(lambda e: add_level_content(1))

# Layout
layout = pn.Column(
    pn.pane.Markdown("# Hierarchical Generation", align='center', styles={'text-align': 'center'}),
    pn.Row(pn.HSpacer(), main_button, pn.HSpacer()),
    pn.Spacer(height=20),
    display_area,
    width=800,
    align='center'
)

if __name__ == '__main__':
    # Launching on 8067
    pn.serve(layout, port=8067)
