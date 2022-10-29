import dash
from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd

dash.register_page(
    __name__
)

df = pd.read_csv("~/CAA/dash/data/colleges.csv")
def show_admission_picture(df, year, state):
    df.dropna(inplace=True)
    df = df[df['State']==state]
    df[f"{year} Admission Rate"] = df[f"{year} Admission Rate"].mul(100)
    fig = px.bar(df, y="Name", x=f"{year} Admission Rate", color="Type", orientation="h", barmode="group")
    fig.update_layout(
        yaxis={"categoryorder": "total descending"},
        title_text="US College Admission Rate",
        height=1500,
    )
    return fig

@callback(
    [
        Output('admission-school-state-graph', 'figure'),
    ],
    [
        Input('admission-year-dropdown', 'value'),
        Input('admission-state-dropdown', 'value')
    ]
)
def _load_admission_picture(year_value, state_value):
    return [show_admission_picture(df, year_value, state_value)]

layout = html.Div(children=[
    html.H1(children='US College Admission Rate'),
    html.P("Filter results in time", style = {'font-size': '16px', 'padding-top': '-0.2vh'}),
    dcc.Dropdown(['Latest', '2019'], 'Latest', id='admission-year-dropdown'),
    dcc.Dropdown([
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL',
        'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE',
        'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD',
        'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'], 'IL', id='adminssion-state-dropdown'),
    dcc.Graph(
       id='admission-school-state-graph',
       figure=show_admission_picture(df, 'Latest', 'IL'),
    )
 ])