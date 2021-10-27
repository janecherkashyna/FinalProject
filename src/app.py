from getengine import engine
from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px


app = Dash(__name__)
server = app.server

df = pd.read_sql_query("SELECT * FROM trips", con=engine)

app.layout = html.Div([
    html.H1(["Tourism statistics in different countries"],
            style={'font-weight': 'bold', "text-align": "center"}),
    html.Br(),
    html.Div([
        dash_table.DataTable(
            columns=[
                {"name": i, "id": i}
                for i in df.columns
            ],
            data=df.to_dict('records'),
            sort_action="native",
            page_action="native",
            page_current=0,
            page_size=8,
            style_cell={
                'minWidth': 95, 'maxWidth': 95, 'width': 95
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'border': '1px solid blue'
            },
            style_header={'border': '1px solid purple'})
        ], className='twelve columns'),

    html.H5(["-All given data about the number of trips or "
             "arrivals is in thousands-"]
            ),
    html.Br(),
    html.Div([
        dcc.Graph(id='our_graph')
    ], className='eight columns'),

    html.Div([

        html.Br(),
        html.Label(['Choose 3 Countries to Compare:'],
                   style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='country_one',
                     options=[{'label': x, 'value': x} for x in
                              df.sort_values('country')['country'].unique()],
                     value='France',
                     multi=False,
                     disabled=False,
                     clearable=True,
                     searchable=True,
                     placeholder='Choose Country...',
                     className='form-dropdown',
                     persistence='string',
                     persistence_type='session'),

        dcc.Dropdown(id='country_two',
                     options=[{'label': x, 'value': x} for x in
                              df.sort_values('country')['country'].unique()],
                     value='Canada',
                     multi=False,
                     disabled=False,
                     clearable=True,
                     searchable=True,
                     placeholder='Choose Country...',
                     className='form-dropdown',
                     persistence='string',
                     persistence_type='session'),

        dcc.Dropdown(id='country_three',
                     options=[{'label': x, 'value': x} for x in
                              df.sort_values('country')['country'].unique()],
                     value='Spain',
                     multi=False,
                     disabled=False,
                     clearable=True,
                     searchable=True,
                     placeholder='Choose Country...',
                     className='form-dropdown',
                     persistence='string',
                     persistence_type='session'),

    ], className='three columns')
])


@app.callback(
    Output('our_graph', 'figure'),
    [Input('country_one', 'value'),
     Input('country_two', 'value'),
     Input('country_three', 'value')]
)
def build_graph(first_country, second_country, third_country):
    df_filtered = df[(df['country'] == first_country) |
                     (df['country'] == second_country) |
                     (df['country'] == third_country)]

    fig = px.line(df_filtered, x="year", y="domestictrips", color='country')
    fig.update_layout(yaxis={'title': 'Number of domestic trips in thousands'},
                      title={'text': 'Tourism inside the countries',
                      'font': {'size': 28}, 'x': 0.5, 'xanchor': 'center'})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
