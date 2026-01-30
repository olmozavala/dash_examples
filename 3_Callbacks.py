"""
This example demonstrates a basic callback implementation with multiple outputs.
It takes two text inputs and updates two different output divs accordingly.
"""
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# https://dash.plot.ly/getting-started-part-2
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='my-in1', value='initial value', type='text'),
    dcc.Input(id='my-in2', value='second value', type='text'),
    html.Div(id='my-out1'),
    html.Div(id='my-out2')
])

## These callbacks, when receive more than a single Input or Output the order is as follows:
# Array of outputs, array of intputs
@app.callback(
    # Output(component_id='my-div', component_property='children'),
    [Output('my-out1', 'children'),
     Output('my-out2', 'children')],
    [Input('my-in1', 'value'),
    Input('my-in2', 'value')]
)
def update_output_div(in1, in2):
    return F"You\'ve entered {in1} and {in2}", F"Second input: {in2}"   # It has two outputs, one for each div


if __name__ == '__main__':
    app.run(debug=True)
