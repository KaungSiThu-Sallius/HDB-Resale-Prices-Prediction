from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import json

external_stylesheets = [dbc.themes.BOOTSTRAP]

dash.register_page(__name__, path='/', external_stylesheets=external_stylesheets)

df = pd.read_csv('data/clean_hdb_resale_data.csv')

with open('data/singapore_town_boundaries.json') as f:
    singapore_geojson = json.load(f)

df['month'] = pd.to_datetime(df['month'])

# Calculate monthly averages
monthly_avg_price = df.groupby('month', as_index=False)['resale_price'].mean()

# Calculate avg price per flat type
flat_avg_price = df.groupby('flat_type', as_index=False)['resale_price'].mean()

# Calculate avg price per town
town_avg_price = df.groupby('town', as_index=False)['resale_price'].mean()

# Calculate avg price per storey
storey_range_price = df.groupby('storey_range')['adjusted_resale_price'].mean().reset_index()

# For Graph 1
price_trend_fig = px.line(x=monthly_avg_price['month'], 
                        y=monthly_avg_price['resale_price'], title='Trend of Average Resale Prices Over Time', labels={'x': 'Year', 'y': 'Average Resale Price'})
price_trend_fig.update_layout(yaxis_range=[300000, monthly_avg_price['resale_price'].max()+100000], title_font=dict(size=22))

# For Graph 2
price_per_flat_fig = px.pie(flat_avg_price, values='resale_price', names='flat_type', hole=.3, title='Resale Price Distribution by Flat Type')
price_per_flat_fig.update_traces(textinfo='percent+label')
price_per_flat_fig.update_layout(title_font=dict(size=20), showlegend=False)

# For Graph 3
price_per_town_fig = px.choropleth(
    town_avg_price,
    geojson=singapore_geojson,
    locations="town",
    featureidkey="properties.town", 
    color="resale_price",
    color_continuous_scale="Blues",
    title="Average Resale Price per Town (HDB Flats)"
)
price_per_town_fig.update_geos(fitbounds="locations", visible=False)
price_per_town_fig.update_layout(title_font=dict(size=20), margin={"r":20, "l":20, "b":40})

# For Graph 4
floor_vs_price_fig = px.scatter(df, x='floor_area_sqm', y='adjusted_resale_price', title='Floor Area(sqm) Vs. Resale Price', labels={'floor_area_sqm': 'Floor Area(sqm)', 'adjusted_resale_price':'Resale Price'})
floor_vs_price_fig.update_traces(marker=dict(size=3, opacity=0.5))
floor_vs_price_fig.update_layout(title_font=dict(size=20))

# For Graph 5
avg_price_flat_fig = px.bar(df['flat_type'].value_counts().reset_index(), x='flat_type', y='count', title='Distribution of Flat Types', labels={'count':'Count', 'flat_type': 'Flat Type'}, text_auto=True)
avg_price_flat_fig.update_layout(height=600, title_font=dict(size=20))

# For Graph 6
storey_price_fig = px.bar(storey_range_price, x='adjusted_resale_price', y='storey_range', title='Avg Resale Price by Storey Range', labels={'adjusted_resale_price':'Adjusted Resale Price', 'storey_range': 'Storey Range'})
storey_price_fig.update_layout(height=600, title_font=dict(size=20))

layout = dbc.Container([
    dbc.Row([
        html.H1(children='Singapore Public Housing (HDB) Resale Price Analysis', className='heading')
    ]),
    dbc.Row([
        # Graph 1
        dbc.Col([
            dcc.Graph(id='price_trend_fig' ,figure=price_trend_fig, className='shadow_box')
        ], width=8),
        dbc.Col([
            dcc.Graph(id='price_per_flat_fig', figure=price_per_flat_fig, className='shadow_box')
        ], width=4)
    ]),
    dbc.Row([
        # Graph 3
        dbc.Col([
            dcc.Graph(id='price_per_town', figure=price_per_town_fig, className='shadow_box'),
            html.Button("Reset Map", id='reset_map', n_clicks=0, className="btn mt-2 reset_btn")
        ], width=6, style={'paddingLeft': '0'}),
        # Graph 4
        dbc.Col([
            dcc.Graph(id='floor_vs_price', figure=floor_vs_price_fig, className='shadow_box')
        ], width=6, style={'paddingRight': '0'})
    ], style={'margin': '40px 0 0 0'}),
    dbc.Row([
        # Graph 5
        dbc.Col([
            dcc.Graph(id='avg_price_flat_fig', figure=avg_price_flat_fig, className='shadow_box'),
        ], width=5, style={'paddingLeft': '0'}),
        # Graph 6
        dbc.Col([
            dcc.Graph(id='storey_price_fig', figure=storey_price_fig, className='shadow_box')
        ], width=7, style={'paddingRight': '0'})
    ], style={'margin': '0 0 40px 0'}),
], className='analysis_page')

@callback(
    Output("price_trend_fig", "figure"), 
    Output("price_per_flat_fig", "figure"),
    Input("price_per_town", "clickData"),
    Input("reset_map", "n_clicks")
)
def updateGraphs(clickData, n_clicks):
    ctx = dash.callback_context
    
    if ctx.triggered and ctx.triggered[0]['prop_id'].startswith("reset_map"):
        return price_trend_fig, price_per_flat_fig
    
    if not clickData:
        return price_trend_fig, price_per_flat_fig
    
    clickedTown = clickData["points"][0]['location']
    
    town_data = df[df["town"] == clickedTown]
    
    town_trend = town_data.groupby("month", as_index=False)["resale_price"].mean()    
    trend_fig = px.line(
                x=town_trend['month'], 
                y=town_trend['resale_price'], 
                title=f'Trend of Average Resale Prices Over Time in {clickedTown}', 
                labels={'x': 'Year', 'y': 'Average Resale Price'}
    )
    trend_fig.update_layout(yaxis_range=[300000, town_trend['resale_price'].max()+100000], title_font=dict(size=22))
    
    town_flat_price = town_data.groupby("flat_type", as_index=False)["resale_price"].mean()
    flat_fig = px.pie(
        town_flat_price, values='resale_price', names='flat_type', hole=.3,title='Resale Price Distribution by Flat Type'
    )
    flat_fig.update_traces(textinfo='percent+label')
    flat_fig.update_layout(title_font=dict(size=20), showlegend=False)

    return trend_fig, flat_fig
