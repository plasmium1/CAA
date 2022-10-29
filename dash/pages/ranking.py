import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
from ast import literal_eval

dash.register_page(
    __name__
)

def earning_salary(list_of_major_earnings, major):
    for major_earning in list_of_major_earnings:
        if major_earning['title'] == f"{major}.":
            return major_earning['earnings']['highest']['3_yr']['overall_median_earnings']

df = pd.read_csv("~/CAA/dash/data/colleges.csv", converters={'latest.programs.cip_4_digit': literal_eval})
subject_names=[]
for myseries in df['latest.programs.cip_4_digit']:
   for s in myseries:
       subject_names.append(s['title'][:-1])
set_subject_names = sorted(set(subject_names))

def show_ranking_picture(df, major, state):
    df['Earning'] = df['latest.programs.cip_4_digit'].apply(lambda x: earning_salary(x, major))
    df1 = df[['Name', 'Earning']].sort_values(by='Earning')
    df1 = df1.dropna()
    if state != "US":
        df1 = df1[df['State']==state]
        ttext = f"{state}: {major} Undergraduate Ranking based on earning"
    if state == "US":
        df1 = df1.tail(20) # top 20 colleges in US
        ttext = f"{state}: Top 20 {major} Undergraduate Ranking based on earning"
    fig = px.bar(df1, y="Name", x="Earning", orientation="h", barmode="group", hover_data={'Earning': ':.d', 'Name': True})
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        title_text=ttext,
        height=1500,
    )
    return fig

@callback(
    [
        Output('school-ranking-graph', 'figure'),
    ],
    [
        Input('field-of-study-dropdown', 'value'),
        Input('state-dropdown', 'value')
    ]
)
def _load_ranking_picture(major_value, state_value):
    return [show_ranking_picture(df, major_value, state_value)]

layout = html.Div(children=[
    html.H1(children='US College Ranking'),
    html.P("US College Scorecard Major Ranking", style = {'font-size': '16px', 'padding-top': '-0.2vh'}),
    dcc.Dropdown(list(set_subject_names), 'Computer Science', id='field-of-study-dropdown'),
    dcc.Dropdown([
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL',
        'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE',
        'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD',
        'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'US'], 'US', id='state-dropdown'),
    dcc.Graph(
       id='school-ranking-graph',
       figure=show_ranking_picture(df, 'Computer Science', 'US'),
    )
])
