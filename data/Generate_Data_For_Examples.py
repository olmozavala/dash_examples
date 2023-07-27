import cmocean
from urllib.request import urlopen
import json
import numpy as np
import pandas as pd

# ------------ Simple markdown example
my_markdown = '''
### Title
Here I talk about some cool stuff, **bold** maybe  some code?

``Python
my code 
``
'''

# ------------- Example in how to get color values from a cmocean colormap
N = 100
cmdict = cmocean.tools.get_dict(cmocean.cm.matter, N=N) # available colorpalettes here
colors_str = ['#%02x%02x%02x' % (int(x[0]*255),int(x[0]*255),int(x[2]*255)) for x in cmdict['red']]

# ---------------- 3D synthetic data
age = [20,23,45]
height= [1.5,1.8,1.9]
weight= np.random.random(3)

# ---------------- Reads the json file with the counties
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

#  This is the dataframe that will be used in the choropleth with association to the counties
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv", dtype={"fips": str})

# ----------------- Surface example
x = np.linspace(-np.pi, np.pi, 20)
X,Y = np.meshgrid(x,x)
Z = np.cos(X) + np.cos(Y)