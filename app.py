import dash
from dash import dcc, html
import pandas as pd
import pickle
from callbacks import get_callbacks

# Load the model
with open('model/car_price_prediction.model', 'rb') as file:
    model = pickle.load(file)

# Import data
df = pd.read_csv('./datasets/data_clean.csv', index_col=0)

# Init Dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# App layout
app.layout = html.Div([
    html.Div([
        html.H3('MODEL UCZENIA MASZYNOWEGO - REGRESYJNY MODEL PRZEWIDYWANIA CENY SAMOCHODÓW UŻYWANYCH',
                style={'color': '#007BFF', 'fontWeight': 'bold'}),
        html.H6('Model lasów losowych (biblioteka sckit learn)',
                style={'color': '#6C757D'})
    ], style={'textAlign': 'center', 'padding': '20px'}),

    html.Hr(),

    dcc.Tabs([
        dcc.Tab(
            label='Model przewidywania cen pojazdów',
            children=[
                html.Label('Podaj rok produkcji samochodu', style={'fontWeight': 'bold'}),
                dcc.Slider(id='slider-1',
                           min=df.Year.min(),
                           max=df.Year.max(),
                           step=1,
                           marks={i: str(i) for i in range(df.Year.min(), df.Year.max() + 1)},
                           tooltip={'placement': 'bottom', 'always_visible': True}),

                html.Div(id='slider-1-output', style={'marginTop': 20}),

                html.Hr(),
                html.Label('Podaj rozmiar silnika', style={'fontWeight': 'bold'}),
                dcc.Slider(id='slider-2',
                           min=df.Engine.min(),
                           max=df.Engine.max(),
                           marks={i: str(i) for i in range(int(df.Engine.min()), int(df.Engine.max()) + 1, 300)},
                           tooltip={'placement': 'bottom', 'always_visible': True}),

                html.Div(id='slider-2-output', style={'marginTop': 20}),

                html.Hr(),
                html.Label('Podaj moc samochodu', style={'fontWeight': 'bold'}),
                dcc.Slider(id='slider-3',
                           min=df.Power.min(),
                           max=df.Power.max(),
                           marks={i: str(i) for i in range(int(df.Power.min()), int(df.Power.max()) + 1, 30)},
                           tooltip={'placement': 'bottom', 'always_visible': True}),

                html.Div(id='slider-3-output', style={'marginTop': 20}),

                html.Hr(),

                html.Div([
                    html.Div([
                        html.Label('Podaj liczbę pasażerów', style={'fontWeight': 'bold'}),
                        dcc.Dropdown(id='drop-1',
                                     options=[{'label': p, 'value': p} for p in sorted(df.Seats.unique())],
                                     placeholder='Wybierz...')
                    ], style={'width': '25%', 'padding': '0 10px'}),

                    html.Div([
                        html.Label('Podaj typ paliwa', style={'fontWeight': 'bold'}),
                        dcc.Dropdown(id='drop-2',
                                     options=[{'label': fuel, 'value': fuel} for fuel in
                                              ['Diesel', 'Benzyna', 'CNG', 'LPG', 'Elektryczne']],
                                     placeholder='Wybierz...')
                    ], style={'width': '25%', 'padding': '0 10px'}),

                    html.Div([
                        html.Label('Podaj typ przekładni', style={'fontWeight': 'bold'}),
                        dcc.Dropdown(id='drop-3',
                                     options=[{'label': trans, 'value': trans} for trans in ['Manualna', 'Automatyczna']],
                                     placeholder='Wybierz...')
                    ], style={'width': '25%', 'padding': '0 10px'})
                ], style={'display': 'flex', 'justify-content': 'space-between'}),

                html.Hr(),
                html.Div([
                    html.H2('Predykcja na podstawie modelu', style={'color': '#007BFF', 'fontWeight': 'bold'}),
                    html.Hr(),
                    html.H3('Podałeś następujące parametry:', style={'color': '#6C757D'}),
                    html.Div(id='div-1',
                             style={'textAlign': 'left', 'marginLeft': '5%', 'fontSize': 18}),
                    html.Hr(),
                    html.Div(id='div-2', style={'fontSize': 24, 'color': '#28A745', 'fontWeight': 'bold'})
                ], style={'textAlign': 'center', 'padding': '20px'})
            ]
        ),

        dcc.Tab(
            label='Wykresy zależności cen pojazdów',
            children=[
                html.Div([
                    html.Div([
                        dcc.Dropdown(id='drop-4',
                                     options=[{'label': 'Rok Produkcji', 'value': 'Year'},
                                              {'label': 'Pojemność silnika', 'value': 'Engine'},
                                              {'label': 'Moc silnika', 'value': 'Power'},
                                              {'label': 'Ilość miejsc', 'value': 'Seats'}],
                                     value='Year',
                                     style={'width': '50%', 'margin': '0 auto', 'padding': '10px'})
                    ],
                        style={'textAlign': 'center', 'padding': '20px'}),

                    html.Div(
                        id='graph-1',
                        style={
                            'display': 'flex',
                            'justify-content': 'space-between',
                        }
                    )
                ],
                style={
                    'width': '80%',
                    'margin': 'auto',
                    'background-color': '#F8F9FA'
                }
                )
            ]

        )
    ])
])

# callbacks
get_callbacks(app, model, df)

if __name__ == '__main__':
    app.run_server(debug=True)
