# 1
# html.H1("HDB Resale Data Analysis", 
    #         style={
    #             "textAlign": "center", 
    #             "color": COLORS['text'], 
    #             "marginBottom": "30px",
    #             "fontWeight": "bold"
    #         }),
    
    # html.Div([
    #     html.Div([
    #         dcc.Graph(
    #             id="price_map",
    #             figure=px.scatter_map(
    #                 town_coordinates,
    #                 lat='latitude',
    #                 lon='longitude',
    #                 size='resale_price',
    #                 color='resale_price',
    #                 hover_name='town',
    #                 hover_data={'resale_price': ':,.2f', 'latitude': False, 'longitude': False},
    #                 color_continuous_scale="Viridis",
    #                 zoom=11,
    #                 title="Average Resale Price by Town",
    #                 size_max=30,
    #                 labels={'resale_price': 'Average Resale Price (SGD)'}
    #             ).update_layout(
    #                 title_x=0.5,
    #                 title_font_size=20,
    #                 mapbox={'style': "carto-positron",
    #                         'center': {'lat': 1.3521, 'lon': 103.8198},
    #                         'zoom': 11},
    #                 paper_bgcolor='white',
    #                 plot_bgcolor='white',
    #                 margin=dict(l=20, r=20, t=40, b=20)
    #             )
    #         ),
    #     ], className="graph-container"),
        
    #     html.Div([
    #         dcc.Graph(
    #             id="price_histogram",
    #             figure=px.histogram(
    #                 df, 
    #                 x="resale_price", 
    #                 nbins=50,
    #                 title="Resale Price Distribution"
    #             ).update_layout(
    #                 title_x=0.5,
    #                 title_font_size=20,
    #                 paper_bgcolor='white',
    #                 plot_bgcolor='white',
    #                 margin=dict(l=20, r=20, t=40, b=20)
    #             )
    #         ),
    #     ], className="graph-container"),
        
    #     html.Div([
    #         dcc.Graph(
    #             id="scatter_plot",
    #             figure=px.scatter(
    #                 df, 
    #                 x="floor_area_sqm", 
    #                 y="resale_price",
    #                 color="flat_type", 
    #                 title="Floor Area vs. Resale Price"
    #             ).update_layout(
    #                 title_x=0.5,
    #                 title_font_size=20,
    #                 paper_bgcolor='white',
    #                 plot_bgcolor='white',
    #                 margin=dict(l=20, r=20, t=40, b=20)
    #             )
    #         ),
    #     ], className="graph-container"),
        
    #     html.Div([
    #         dcc.Graph(
    #             id="boxplot",
    #             figure=px.box(
    #                 df, 
    #                 x="town", 
    #                 y="resale_price",
    #                 title="Price Distribution by Town"
    #             ).update_layout(
    #                 title_x=0.5,
    #                 title_font_size=20,
    #                 paper_bgcolor='white',
    #                 plot_bgcolor='white',
    #                 margin=dict(l=20, r=20, t=40, b=20),
    #                 xaxis_tickangle=-45
    #             )
    #         )
    #     ], className="graph-container"),
    # ], style={
    #     "display": "grid",
    #     "gridTemplateColumns": "repeat(2, 1fr)",
    #     "gap": "20px",
    #     "padding": "20px"
    # })
    
    
    
# 2
# Prepare data for map visualization
# town_avg_prices = df.groupby('town')['resale_price'].mean().reset_index()
# town_coordinates = df.groupby('town').agg({
#     'latitude': 'mean',
#     'longitude': 'mean',
#     'resale_price': 'mean'
# }).reset_index()

# 📌 Layout for Data Analysis Page
# Add these constants for consistent styling

import dash
from dash import dcc, html, Input, Output, State, no_update
import plotly.express as px
import pandas as pd
import pickle
import numpy as np

# Load dataset
df = pd.read_csv("data/clean_hdb_resale_data.csv")

# Load trained XGBoost model
with open("data/model/xgb_model.pkl", "rb") as file:
    model = pickle.load(file)

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "HDB Resale Price Prediction"

# Create header with navigation
header = html.Div([
    html.Div([
        html.Button(
            "Analysis", 
            id="nav-analysis",
            n_clicks=0,
            style={
                "backgroundColor": "#3498db",
                "color": "white",
                "padding": "10px 20px",
                "border": "none",
                "borderRadius": "5px",
                "marginRight": "10px"
            }
        ),
        html.Button(
            "Price Prediction", 
            id="nav-prediction",
            n_clicks=0,
            style={
                "backgroundColor": "#3498db",
                "color": "white",
                "padding": "10px 20px",
                "border": "none",
                "borderRadius": "5px"
            }
        )
    ], style={"textAlign": "center", "marginBottom": "20px"})
])

# Prepare data for map visualization
town_avg_prices = df.groupby('town')['resale_price'].mean().reset_index()
town_coordinates = df.groupby('town').agg({
    'latitude': 'mean',
    'longitude': 'mean',
    'resale_price': 'mean'
}).reset_index()

# 📌 Layout for Data Analysis Page
# Add these constants for consistent styling
COLORS = {
    'primary': '#3498db',
    'secondary': '#2ecc71',
    'background': '#f8f9fa',
    'text': '#2c3e50'
}

analysis_layout = html.Div([
    html.H1("HDB Resale Data Analysis", 
            style={
                "textAlign": "center", 
                "color": COLORS['text'], 
                "marginBottom": "30px",
                "fontWeight": "bold"
            }),
    
    html.Div([
        html.Div([
            dcc.Graph(
                id="price_map",
                figure=px.scatter_map(
                    town_coordinates,
                    lat='latitude',
                    lon='longitude',
                    size='resale_price',
                    color='resale_price',
                    hover_name='town',
                    hover_data={'resale_price': ':,.2f', 'latitude': False, 'longitude': False},
                    color_continuous_scale="Viridis",
                    zoom=11,
                    title="Average Resale Price by Town",
                    size_max=30,
                    labels={'resale_price': 'Average Resale Price (SGD)'}
                ).update_layout(
                    title_x=0.5,
                    title_font_size=20,
                    mapbox={'style': "carto-positron",
                            'center': {'lat': 1.3521, 'lon': 103.8198},
                            'zoom': 11},
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    margin=dict(l=20, r=20, t=40, b=20)
                )
            ),
        ], className="graph-container"),
        
        html.Div([
            dcc.Graph(
                id="price_histogram",
                figure=px.histogram(
                    df, 
                    x="resale_price", 
                    nbins=50,
                    title="Resale Price Distribution"
                ).update_layout(
                    title_x=0.5,
                    title_font_size=20,
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    margin=dict(l=20, r=20, t=40, b=20)
                )
            ),
        ], className="graph-container"),
        
        html.Div([
            dcc.Graph(
                id="scatter_plot",
                figure=px.scatter(
                    df, 
                    x="floor_area_sqm", 
                    y="resale_price",
                    color="flat_type", 
                    title="Floor Area vs. Resale Price"
                ).update_layout(
                    title_x=0.5,
                    title_font_size=20,
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    margin=dict(l=20, r=20, t=40, b=20)
                )
            ),
        ], className="graph-container"),
        
        html.Div([
            dcc.Graph(
                id="boxplot",
                figure=px.box(
                    df, 
                    x="town", 
                    y="resale_price",
                    title="Price Distribution by Town"
                ).update_layout(
                    title_x=0.5,
                    title_font_size=20,
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    margin=dict(l=20, r=20, t=40, b=20),
                    xaxis_tickangle=-45
                )
            )
        ], className="graph-container"),
    ], style={
        "display": "grid",
        "gridTemplateColumns": "repeat(2, 1fr)",
        "gap": "20px",
        "padding": "20px"
    })
], style={"backgroundColor": COLORS['background'], "padding": "20px"})

# Update prediction layout styling
prediction_layout = html.Div([
    html.H1("HDB Resale Price Prediction", 
            style={
                "textAlign": "center", 
                "color": COLORS['text'], 
                "marginBottom": "30px",
                "fontWeight": "bold"
            }),
    
    html.Div([
        html.Div([
            html.Label("Town", style={"fontWeight": "bold", "color": COLORS['text']}),
            dcc.Dropdown(
                id="town",
                options=[{"label": t, "value": t} for t in df["town"].unique()],
                placeholder="Select Town",
                style={"marginBottom": "20px"}
            ),

            html.Label("Floor Area (sqm)"),
            dcc.Input(
                id="floor_area", 
                type="number",
                placeholder="Enter Floor Area (sqm)",
                style={"width": "100%", "marginBottom": "20px"}
            ),

            html.Label("Flat Type"),
            dcc.Dropdown(
                id="flat_type",
                options=[{"label": t, "value": t} for t in df["flat_type"].unique()],
                placeholder="Select Flat Type",
                style={"marginBottom": "20px"}
            ),

            html.Label("Flat Model"),
            dcc.Dropdown(
                id="flat_model",
                options=[{"label": t, "value": t} for t in df["flat_model"].unique()],
                placeholder="Select Flat Model",
                style={"marginBottom": "20px"}
            ),

            html.Button(
                "Predict Price", 
                id="predict-btn", 
                n_clicks=0,
                style={
                    "backgroundColor": "#2ecc71",
                    "color": "white",
                    "padding": "10px 20px",
                    "border": "none",
                    "borderRadius": "5px",
                    "width": "100%",
                    "marginTop": "20px"
                }
            ),

            html.Div(
                id="prediction-output",
                style={
                    "marginTop": "20px",
                    "padding": "20px",
                    "backgroundColor": "#f8f9fa",
                    "borderRadius": "5px",
                    "textAlign": "center"
                }
            )
        ], style={
            "width": "50%",
            "margin": "0 auto",
            "padding": "30px",
            "backgroundColor": "white",
            "borderRadius": "10px",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
        })
    ])
], style={"backgroundColor": COLORS['background'], "padding": "20px", "minHeight": "100vh"})

# 📌 Main Layout with Page Navigation
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    header,
    html.Div(id="page-content")
])

# 📌 Callback for Page Navigation
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if (pathname == "/prediction"):
        return prediction_layout
    return analysis_layout  # Default page

# 📌 Callback for Button Navigation
@app.callback(
    Output("url", "pathname"),
    [Input("nav-analysis", "n_clicks"), 
     Input("nav-prediction", "n_clicks")]
)
def navigate(n1, n2):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "nav-prediction":
        return "/prediction"
    elif button_id == "nav-analysis":
        return "/"
    return no_update

# 📌 Callback for Price Prediction
@app.callback(
    Output("prediction-output", "children"),
    Input("predict-btn", "n_clicks"),
    State("town", "value"),
    State("floor_area", "value"),
    State("flat_type", "value"),
    State("flat_model", "value")
)
def predict_price(n_clicks, town, floor_area, flat_type, flat_model):
    if n_clicks == 0:
        return ""
    
    if not all([town, floor_area, flat_type, flat_model]):
        return "Please fill in all fields!"

    try:
        # Create input data for prediction
        input_data = pd.DataFrame({
            'town': [town],
            'floor_area_sqm': [floor_area],
            'flat_type': [flat_type],
            'flat_model': [flat_model]
        })
        
        # Make prediction
        prediction = model.predict(input_data)
        
        # Format prediction
        predicted_price = f"S${prediction[0]:,.2f}"
        return f"Estimated Resale Price: {predicted_price}"
    
    except Exception as e:
        return f"Error in prediction: {str(e)}"

# 📌 Callback for Button Navigation
@app.callback(
    [Output("nav-analysis", "style"),
     Output("nav-prediction", "style")],
    Input("url", "pathname")
)
def update_nav_style(pathname):
    base_style = {
        "backgroundColor": "#3498db",
        "color": "white",
        "padding": "10px 20px",
        "border": "none",
        "borderRadius": "5px",
        "marginRight": "10px",
        "transition": "all 0.3s ease"
    }
    
    active_style = {
        **base_style,
        "borderBottom": "3px solid white",
        "backgroundColor": "#2980b9"
    }
    
    if pathname == "/prediction":
        return [base_style, active_style]
    return [active_style, base_style]

if __name__ == '__main__':
    app.run_server(debug=True)
# Add this at the end of the file
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                margin: 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            }
            .graph-container {
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                padding: 15px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
