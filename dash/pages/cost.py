import dash
from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json
import numpy as np

dash.register_page(
    __name__
)

df = pd.read_csv("~/CAA/dash/data/colleges.csv")
def show_cost_picture(year, state):
    df.dropna(inplace=True)
    if "US" in state:
        dff = df
    else:
        dff=df.loc[df["State"]==state]
    fig = px.scatter_geo(dff[[f"{year} Total Cost", f"{year} Admission Rate", "Name", "Latitude", "Longitude"]],
                         lat="Latitude",
                         lon="Longitude",
                         size=f"{year} Total Cost",
                         color=f"{year} Admission Rate",
                         scope="usa",
                         locationmode = 'USA-states',
                         hover_name="Name")
    if "US" not in state:
        fig.update_geos(fitbounds="locations")
    fig.update_layout(
        title_text="college cost and admission rate",
        height=1500,
        width=1500,
    )
    return fig

@callback(
    [
        Output('cost-scatter-geo', 'figure'),
    ],
    [
        Input('cost-year-dropdown', 'value'),
        Input('cost-state-dropdown', 'value')
    ]
)

def _load_cost_picture(year_value, state_value):
    return [show_cost_picture(year_value, state_value)]

layout = html.Div(children=[
    html.H1(children='US College Overall Cost'),
    html.P("Filter results in time", style = {'font-size': '16px', 'padding-top': '-0.2vh'}),
    dcc.Dropdown(['Latest', '2019'], 'Latest', id='cost-year-dropdown'),
    dcc.Dropdown([
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL',
        'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE',
        'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD',
        'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'US'], 
        id='cost-state-dropdown',
        value="US",
    ),
    dcc.Graph(
       id='cost-scatter-geo',
       figure=show_cost_picture("Latest", "US"),
    )
 ])