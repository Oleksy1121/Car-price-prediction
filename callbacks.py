from dash.dependencies import Input, Output
from dash import html
import pandas as pd


def get_callbacks(app, model):
    @app.callback(
        Output('div-1', 'children'),
        [Input('slider-1', 'value'),
         Input('slider-2', 'value'),
         Input('slider-3', 'value'),
         Input('drop-1', 'value'),
         Input('drop-2', 'value'),
         Input('drop-3', 'value')]
    )
    def display_parameters(val_1, val_2, val_3, val_4, val_5, val_6):
        children = [html.Div(f'Rok Produkcji: {val_1}') if val_1 is not None else None,
                    html.Div(f'Pojemność silnika: {val_2}') if val_2 is not None else None,
                    html.Div(f'Moc: {val_3}') if val_3 is not None else None,
                    html.Div(f'Liczba osób: {val_4}') if val_4 is not None else None,
                    html.Div(f'Typ paliwa: {val_5}') if val_5 is not None else None,
                    html.Div(f'Rodzaj skrzyni biegów: {val_6}') if val_6 is not None else None]
        return children


    fuel_map = {'Diesel': 'Fuel_Type_Diesel', 'Elektryczne': 'Fuel_Type_Electric', 'LPG': 'Fuel_Type_LPG',
                'Benzyna': 'Fuel_Type_Petrol'}


    @app.callback(
        Output('div-2', 'children'),
        [Input('slider-1', 'value'),
         Input('slider-2', 'value'),
         Input('slider-3', 'value'),
         Input('drop-1', 'value'),
         Input('drop-2', 'value'),
         Input('drop-3', 'value')]
    )
    def predict_value(val_1, val_2, val_3, val_4, val_5, val_6):
        if val_1 and val_2 and val_3 and val_4 and val_5 and val_6:
            common_params = {'Year': val_1, 'Engine': val_2, 'Power': val_3, 'Seats': val_4}
            fuel_params = {val: 1 if key in val_5 else 0 for key, val in fuel_map.items()}
            transmission_params = {'Transmission_Manual': 1 if val_6 == 'manual' else 0}
            full_params = {**common_params, **fuel_params, **transmission_params}
            df_sample = pd.DataFrame([full_params])

            price = model.predict(df_sample)[0]
            price = round(price * 1000, 2)
            price = f'{price:,.2f} $'.replace(',', ' ')

            return html.H3(f'Przewidywana cena pojazdu to: {price}')
