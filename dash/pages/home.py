import dash
from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json

dash.register_page(
    __name__,
    path='/',
    title="US College Insights",
    name="College Ranking - SAT"
)

def show_sat_picture(df, year, state):
    df.dropna(inplace=True)
    df = df[df['State']==state]
    fig = px.bar(df, y="Name", x=f"{year} SAT Average", color="Type", orientation="h", barmode="group")
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        title_text="US College Ranking - SAT",
        height=1500,
    )
    return fig

@callback(
    [
        Output('school-state-graph', 'figure'),
    ],
    [
        Input('year-dropdown', 'value'),
        Input('state-dropdown', 'value')
    ]
)
def _load_sat_picture(year_value, state_value):
    return [show_sat_picture(df, year_value, state_value)]

df = pd.read_csv("~/CAA/dash/data/colleges.csv")

layout = html.Div(children=[
    html.H1(children='US College Ranking - SAT'),
    html.P("Filter results in time", style = {'font-size': '16px', 'padding-top': '-0.2vh'}),
    dcc.Dropdown(['Latest', '2019'], 'Latest', id='year-dropdown'),
    dcc.Dropdown(id="state-dropdown", options=df["State"].unique(), value="IL"),
    dcc.Graph(
       id='school-state-graph',
       figure=show_sat_picture(df, 'Latest', 'IL'),
    )
 ])