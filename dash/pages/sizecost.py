import dash
from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd

dash.register_page(
    __name__
)

df = pd.read_csv("~/CAA/dash/data/colleges.csv")
df1 = df[["State", "City", "Name", "Latest Student Size", "2019 Total Cost"]].dropna()
def show_overview_picture(pic_type):
    if pic_type == "Sunburst":
        fig = px.sunburst(
            df1, 
            path=[px.Constant("Number of College Students"), "State", "City", "Name"],
            values="Latest Student Size",
            color="2019 Total Cost",
            color_continuous_scale="tealrose",
        )
    else:
        fig = px.treemap(
            df1,
            path=[px.Constant("Number of College Students"), "State", "City", "Name"],
            values="Latest Student Size",
            color="2019 Total Cost",
            color_continuous_scale="tealrose",
        )
    fig.update_layout(
        title_text="college student size and cost",
        height=1500,
        width=1500,
    )
    return fig


layout = html.Div([
    html.H1(children='Student Size and College Cost Graph'),
    dcc.Tabs(id='tabs-student-size-cost', value='sunburst', children=[
        dcc.Tab(label='Sunburst', value='sunburst'),
        dcc.Tab(label='Treemap', value='treemap'),
    ]),
    html.Div(id='div-student-size-cost')
])

@callback(
    Output('div-student-size-cost', 'children'),
    Input('tabs-student-size-cost', 'value')
)
def render_content(tab):
    if tab == 'sunburst':
        return html.Div([
            dcc.Graph(
                figure=show_overview_picture("Sunburst"),
            )
        ])
    elif tab == 'treemap':
        return html.Div([
            dcc.Graph(
                figure=show_overview_picture("Treemap"),
            )
        ])