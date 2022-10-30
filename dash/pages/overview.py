import dash
from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)

    return fig

dash.register_page(
    __name__
)

df = pd.read_csv("~/CAA/dash/data/colleges.csv")

num_of_colleges = df["Name"].count()

num_of_public = df.groupby(['Type']).size()["Public"]
num_of_private_forprofit = df.groupby(['Type']).size()["Private ForProfit"]
num_of_private_nonprofit = df.groupby(['Type']).size()["Private NonProfit"]

# Card components
cards = [
    dbc.Card(
        [
            html.H2(f"{num_of_colleges}", className="card-title"),
            html.P("Total Colleges", className="card-text"),
        ],
        body=True,
        color="light",
    ),
    dbc.Card(
        [
            html.H2(f"{num_of_public}", className="card-title"),
            html.P("Public", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    ),
    dbc.Card(
        [
            html.H2(f"{num_of_private_nonprofit}", className="card-title"),
            html.P("Private For Profit", className="card-text"),
        ],
        body=True,
        color="primary",
        inverse=True,
    ),
    dbc.Card(
        [
            html.H2(f"{num_of_private_forprofit}", className="card-title"),
            html.P("Private", className="card-text"),
        ],
        body=True,
        color="blue",
        inverse=True,
    ),
]

@callback(
    [
        Output("school-mapbox-id", "figure"),
        Output("school-table-div-id", "children"),
    ],
    Input("dropdown-school-id", "value"),
)
def update_figures(school):

    selected_df=df.loc[df["Name"]==school]
    selected_df= selected_df.fillna("Unreleased Data")
    mapbox_fig = px.scatter_mapbox(
        selected_df[[
            "Latest Total Cost",
            "Latest Admission Rate",
            "Latest Student Size",
            "Median Earnings",
            "Graduation Rate",
            "Average Cost",
            "Latest SAT Average",
            "Name",
            "Latitude",
            "Longitude"
            ]],
        lat="Latitude",
        lon="Longitude",
        size="Latest Student Size",
        hover_name="Name", 
        hover_data=[
            "Latest Total Cost",
            "Latest Admission Rate",
            "Latest Student Size",
            "Median Earnings",
            "Graduation Rate",
            "Average Cost",
            "Latest SAT Average"
        ],
        zoom=4,
        title = f"Map for {school}",
    )
    mapbox_fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":50,"l":0,"b":10},
    )
    school_url = df[df['Name'] == school]['URL'].values[0]
    school_url = school_url.replace("https://", "")
    price_url = df[df['Name'] == school]['Price Calculator'].values[0]
    price_url = price_url.replace("https://","")
    table_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th(
                        html.A(f"{school} Homepage", href=f"http://{school_url}", target="_blank")
                    )
                ]
            ),
            style={'text-align':'center'}, 
        )
    ]
    table_body = [
        html.Tbody(
            [
                html.Tr([html.Td("Graduation Rate"), html.Td(df[df['Name'] == school]['Graduation Rate'].values[0])]),
                html.Tr([html.Td("Median Earnings"), html.Td(df[df['Name'] == school]['Median Earnings'].values[0])]),
                html.Tr([html.Td("Total Cost"), html.Td(df[df['Name'] == school]['Latest Total Cost'].values[0])]),
                html.Tr([html.Td("Average Cost"), html.Td(df[df['Name'] == school]['Average Cost'].values[0])]),
                html.Tr([html.Td("Student Size"), html.Td(df[df['Name'] == school]['Latest Student Size'].values[0])]),
                html.Tr([html.Td("SAT Average"), html.Td(df[df['Name'] == school]['Latest SAT Average'].values[0])]),
            ]
        )
    ]
    table_foot = [
        html.Tfoot(
            html.A(f"{school}: School Price Calculator", href=f"http://{price_url}", target="_blank"),
            style={'text-align':'center'},
        )
    ]
    table_fig = dbc.Table(
        table_header + table_body + table_foot,
        bordered=False,
        hover=True,
        responsive=True,
        striped=True,
    )
    return mapbox_fig, table_fig

layout = dbc.Container(
    [
        html.Hr(),
        dbc.Row([dbc.Col(card) for card in cards]),
        html.Br(),
        html.Br(),
        html.H1(children='Type school name to search college', style={'text-align':'center'}),
        html.Br(),
        dbc.Row(
            [
                dcc.Dropdown(
                    id="dropdown-school-id",
                    options=df["Name"].sort_values(),
                ),
            ],
        ),
        html.Div(id="school-table-div-id"),
        dbc.Row(
            [
               dcc.Graph(id="school-mapbox-id", figure = blank_fig()),
            ],
        ),
    ],
    fluid=False,
)
