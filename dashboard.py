import dash
from dash import Dash, html, dcc
import pandas as pd
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.CERULEAN]

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

server = app.server 

button_container_style = {
    'display': 'flex',
    'gap': '1rem'
}

app.layout = html.Div([
    # Navigation Bar
    html.Nav([
        # Logo
        html.Img(src='assets/logo.png', className="logo_style"),
        html.Div([
            dcc.Link(html.Button('Analysis', className='btn'), href='/'),
            dcc.Link(html.Button('Prediction', className='btn'), href='/prediction')
        ], style=button_container_style)
    ], className='nav'),
    
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
