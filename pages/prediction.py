from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from datetime import datetime
import joblib
import numpy as np
import os
from pathlib import Path

external_stylesheets = [dbc.themes.BOOTSTRAP]

dash.register_page(__name__)

town_mrt_distance = pd.read_csv('data/town_mrt_distances.csv')

try:
    MODEL_PATH = Path(__file__).parent.parent / 'data' / 'model' / 'xgb_random_search_model.pkl'
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

town_list = ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH', 
            'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG',
            'CLEMENTI', 'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
            'KALLANG', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL', 'QUEENSTOWN',
            'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES', 'TOA PAYOH',
            'WOODLANDS', 'YISHUN']

storey_range = ['01 TO 03', '04 TO 06', '07 TO 09', '10 TO 12', 
'13 TO 15', '16 TO 18', '19 TO 21', '22 TO 24', '25 TO 27', '28 TO 30', '31 TO 33', 
'34 TO 36', '37 TO 39', '40 TO 42', '43 TO 45', '46 TO 48', '49 TO 51']

current_month = datetime.now().month

flat_type = ['1 ROOM', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', 'MULTI-GENERATION']

flat_model = ['2-room', '3Gen', 'Adjoined flat', 'Apartment', 'DBSS',
            'Improved', 'Improved-Maisonette', 'Maisonette', 'Model A',
            'Model A-Maisonette', 'Model A2', 'Multi Generation',
            'New Generation', 'Premium Apartment', 'Premium Apartment Loft',
            'Premium Maisonette', 'Simplified', 'Standard', 'Terrace',
            'Type S1', 'Type S2']

layout = dbc.Container([
    dbc.Row([
        html.H1(children='Resale Price Prediction', className='heading')
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Town", html_for="town"),
                        dcc.Dropdown(
                            id='town',
                            options=[
                                {
                                    "label": town, 'value': town
                                } for town in town_list
                            ],
                            placeholder= 'Select a town...',
                            className="mb-3"
                        )
                    ]) 
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Floor Area (sqm)", html_for="floorArea"),
                        dbc.Input(
                            type="number",
                            id="floorArea",
                            placeholder="Enter floor area...",
                            className="mb-3",
                            min=0,
                            max=280,
                            step=1 
                        )
                    ])
                ]),
                dbc.Row([
                    dbc.Col([  
                        dbc.Label("Floor Level", html_for="floorLevel"),
                        dcc.Dropdown(
                            id='floorLevel',
                            options=[
                                {
                                    "label": level, 'value': level
                                } for level in storey_range
                            ],
                            placeholder= 'Select a floor level...',
                            className="mb-3"
                        )
                    ], width=12),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Flat Type", html_for="flatType"),
                        dcc.Dropdown(
                            id='flatType',
                            options=[
                                {
                                    "label": flat, 'value': flat
                                } for flat in flat_type
                            ],
                            placeholder= 'Select a flat type...',
                            className="mb-3"
                        )
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Flat Model", html_for="flatModel"),
                        dcc.Dropdown(
                            id='flatModel',
                            options=[
                                {
                                    "label": _flat_model, 'value': _flat_model
                                } for _flat_model in flat_model
                            ],
                            placeholder= 'Select a flat model...',
                            className="mb-3"
                        )
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Lease Remaining", html_for="lease"),
                        dbc.Input(
                            type="number",
                            id="lease",
                            placeholder="Enter remaining lease years...",
                            className="mb-5",
                            min=0,
                            max=99
                        )
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Button("Predict Price", id="predict-button", className="btn")
                    ], className="text-center")
                ]),
                html.Div(id='prediction-result', className='result_display')
            ], className='predictionForm')
        ])
    ])
], className='prediction_page')

@dash.callback(
    Output('prediction-result', 'children'),
    Input('predict-button', 'n_clicks'),
    [
        State('town', 'value'),
        State('floorArea', 'value'),
        State('floorLevel', 'value'),
        State('flatType', 'value'),
        State('flatModel', 'value'),
        State('lease', 'value'),
    ]
)
def predict(n_clicks, town, floorArea, floorLevel, flatType, flatModel, lease):
    if n_clicks is None:
        return ""
    
    if not all([town, floorArea, floorLevel, flatType, flatModel, lease]):
        return html.Div("Please fill in all fields", style={'color': 'red'})

    
    distance_km = town_mrt_distance[town_mrt_distance['town'] == town]['distance_km'].values[0]
    
    flatTypeList = [f"flat_type_{flat}" for flat in flat_type]
    flatTypeFeature = {flat: 0 for flat in flatTypeList}
    
    townList = [f"town_{town}" for town in town_list]
    townFeatures = {town: 0 for town in townList}
    
    flatModelList = [f"flat_model_{model}" for model in flat_model]
    flatModelFeatures = {model: 0 for model in flatModelList}
    
    flatTypeFeature["flat_type_"+flatType] = 1
    townFeatures["town_"+town] = 1
    flatModelFeatures["flat_model_"+flatModel] = 1
    

    minLevelFloor = int(floorLevel.split(' TO ')[0])
    maxLevelFloor = int(floorLevel.split(' TO ')[1])
    
    inputFeatures = np.array([[
        floorArea, lease, distance_km, current_month, minLevelFloor, maxLevelFloor, flatTypeFeature['flat_type_2 ROOM'],
        flatTypeFeature['flat_type_3 ROOM'], flatTypeFeature['flat_type_4 ROOM'], flatTypeFeature['flat_type_5 ROOM'], flatTypeFeature['flat_type_EXECUTIVE'],
        flatTypeFeature['flat_type_MULTI-GENERATION'],     townFeatures['town_BEDOK'], townFeatures['town_BISHAN'], townFeatures['town_BUKIT BATOK'], 
        townFeatures['town_BUKIT MERAH'], townFeatures['town_BUKIT PANJANG'], townFeatures['town_BUKIT TIMAH'], townFeatures['town_CENTRAL AREA'], 
        townFeatures['town_CHOA CHU KANG'], townFeatures['town_CLEMENTI'], townFeatures['town_GEYLANG'], townFeatures['town_HOUGANG'], 
        townFeatures['town_JURONG EAST'], townFeatures['town_JURONG WEST'], townFeatures['town_KALLANG'], townFeatures['town_MARINE PARADE'],
        townFeatures['town_PASIR RIS'], townFeatures['town_PUNGGOL'], townFeatures['town_QUEENSTOWN'], townFeatures['town_SEMBAWANG'],
        townFeatures['town_SENGKANG'], townFeatures['town_SERANGOON'], townFeatures['town_TAMPINES'], townFeatures['town_TOA PAYOH'],
        townFeatures['town_WOODLANDS'], townFeatures['town_YISHUN'],         flatModelFeatures['flat_model_3Gen'],
        flatModelFeatures['flat_model_Adjoined flat'], flatModelFeatures['flat_model_Apartment'], flatModelFeatures['flat_model_DBSS'],
        flatModelFeatures['flat_model_Improved'], flatModelFeatures['flat_model_Improved-Maisonette'], flatModelFeatures['flat_model_Maisonette'],
        flatModelFeatures['flat_model_Model A'], flatModelFeatures['flat_model_Model A-Maisonette'], flatModelFeatures['flat_model_Model A2'],
        flatModelFeatures['flat_model_Multi Generation'], flatModelFeatures['flat_model_New Generation'], flatModelFeatures['flat_model_Premium Apartment'],
        flatModelFeatures['flat_model_Premium Apartment Loft'], flatModelFeatures['flat_model_Premium Maisonette'], flatModelFeatures['flat_model_Simplified'],
        flatModelFeatures['flat_model_Standard'], flatModelFeatures['flat_model_Terrace'], flatModelFeatures['flat_model_Type S1'],
        flatModelFeatures['flat_model_Type S2']
        ]])

    prediction = model.predict(inputFeatures)
    price = round(prediction[0])
    prediction_result = f"S$ {price:,.0f}"
    
    return html.Div([
        html.H4(f"Predicted Resale Price is ", style={'color': '#7A695B'}),
        html.Div([
            html.H4(prediction_result, style={
                'fontWeight': 'bold',
                'color': '#7A695B'
            })
        ])
    ])
