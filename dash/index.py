import os
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# default bootstrap theme
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "color": "#7F7F7F",
    "background-color": "#EBEBEB",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.Br(),
        html.Br(),
        html.A(
            html.Img(
                src=app.get_asset_url('CAA.png'), height="110px"
            ),
            title="College Admission Assistant",
            href="/overview",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Overview", href="/overview", active="exact"),
                dbc.NavLink("Ranking - Earning", href="/ranking", active="exact"),
                dbc.NavLink("Ranking - SAT", href="/", active="exact"),
                dbc.NavLink("Student Size/Cost", href="/sizecost", active="exact"),
                dbc.NavLink("Admission Rate", href="/admissions", active="exact"),
                dbc.NavLink("Cost Overview", href="/cost", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

navbar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        "College Scorecard", href="https://collegescorecard.ed.gov/", target="_blank",
                        className="ms-5",
                        style={'color': '#EEEEEE', 'font-size': '18px', 'font-weight': 'bold'}
                    )
                ),
            ],
            align="left",
            className="ms-1"
        ),
    ],
    sticky="top",
    color="dark"
)

content = html.Div(dash.page_container, style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, navbar, content])
