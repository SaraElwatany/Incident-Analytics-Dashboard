import datetime
import pandas as pd   
from joblib import load      

# Dash Components Related Modules
import plotly.graph_objects as go
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc 
from dash import Dash, html, dcc, Input, Output, State, callback

# User-Defined Modules
from data import data_preprocess
from tools import monthly_casualties, forecast_interval, get_casualties_features, get_accidents_features


# Read the dataframe
accidents_df = data_preprocess('dataset/global_traffic_accidents.csv')

# Load Feature Columns Names used in training
assessment_feature_columns = load(open('models/assessment_feature_columns.pkl', 'rb'))

# Load ML Models
assessment_model = load('models/assessment_model.pkl')
casualties_forecast_model = load('models/casualties_forecasting_model.pkl')
accidents_forecast_model = load('models/accidents_forecasting_model.pkl')


def create_forecast_layout():

    layout = html.Div([

        # Dropdown to select model type
        html.Div([
            html.Label("Choose A Task From Below:", style={"font-weight": "bold"}),
            dcc.Dropdown(
                id="model-dropdown",
                options=[
                    {"label": "Assess Accident", "value": "assess_accident"},
                    {"label": "Forecast Global Casualties", "value": "forecast_casualties"},
                    {"label": "Forecast Global Accidents", "value": "forecast_accidents"}
                ],
                value="assess_accident",
                clearable=False,
                style={"width": "50%"}
            )
        ], style={"margin-bottom": "20px"}),

        # Dynamic content container
        html.Div(id="main-content-container")

    ], style={"padding": "70px"})

    return layout


@callback(
    Output("main-content-container", "children"),
    Input("model-dropdown", "value")
)
def update_main_layout(selected_model):
    
    if selected_model in ["forecast_casualties", "forecast_accidents"]:
        
        title = "Forecasting Monthly Global Casualties" if selected_model == "forecast_casualties" else "Forecasting Monthly Global Accidents"
        
        # Generate initial historical plot
        if selected_model == "forecast_casualties":
            monthly_counts, _ = get_casualties_features(accidents_df)
            x_col, y_col = monthly_counts['YearMonth'], monthly_counts['Casualties']
            y_title = 'Casualties'
        else:  # forecast_accidents
            monthly_counts, _ = get_accidents_features(accidents_df)
            x_col, y_col = monthly_counts['YearMonth'], monthly_counts['AccidentsCount']
            y_title = 'Accidents'
        
        # Create initial historical plot
        initial_fig = go.Figure()
        initial_fig.add_trace(go.Scatter(
            x=x_col, 
            y=y_col, 
            mode='lines+markers', 
            line=dict(color='#001f3f'), 
            marker=dict(color='#001f3f'),  
            name='Historical'
        ))
        initial_fig.update_layout(
            title='', 
            xaxis_title='Date', 
            yaxis_title=y_title, 
            template='plotly_white'
        )
        
        # Layout for forecasting models - slider above, plot below (full width)
        return html.Div([
            
            # Row for slider controls
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Label("Number of Months to Forecast", style={"fontWeight": "bold", "marginBottom": "15px"}),
                        dcc.Slider(
                            id="month-slider",
                            min=0,
                            max=12,
                            step=1,
                            value=0,
                            marks={i: f"{i}" for i in range(1, 13)},
                        )
                    ], style={"padding": "20px", "marginBottom": "20px"})
                ], width=6),
                
                # Empty column for spacing/future use
                dbc.Col([
                    html.Div()  # Empty div for potential future controls
                ], width=6)
            ]),
            
            # Row for the plot (full width)
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H5(title,
                                id="forecast-card-title",
                                className="card-title text-center mt-3",
                                style={"fontWeight": "bold"}
                            ),
                        dcc.Graph(id="main-forecast-graph", figure=initial_fig)
                    ], className="mb-4 p-3", style={"border": "1px solid #001f3f", "borderRadius": "20px"})
                ], width=12)
            ])
        ])
    
    elif selected_model == "assess_accident":
        
        # Layout for assessment model - original side-by-side layout
        title = "Global Monthly Average Casualties" 
        fig = monthly_casualties(accidents_df, '')
        
        return dbc.Row([
            
            # Left: Styled Graph
            dbc.Col(
                dbc.Card([
                    html.H5(title,
                            id="forecast-card-title",
                            className="card-title text-center mt-3",
                            style={"fontWeight": "bold"}
                        ),
                    dcc.Graph(id="main-forecast-graph", figure=fig)
                ], className="mb-4 p-3", style={"border": "1px solid #001f3f", "borderRadius": "20px"}),
                width=8
            ),

            # Right: Assessment inputs
            dbc.Col([
                html.Div([
                    html.H4("Accident Assessment Inputs", style={"fontWeight": "bold", "marginBottom": "20px"}),

                    html.Label("Select Country", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        options=[{'label': c, 'value': c} for c in sorted(accidents_df['Country'].unique())],
                        id="country-dropdown"
                    ),

                    html.Br(),

                    html.Label("Select City", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        options= [],
                        id="city-dropdown"
                    ),

                    html.Br(),

                    html.Div([
                        html.Div([
                            html.Label("Longitude", style={"fontWeight": "bold"}),
                            dcc.Input(type="number", id="long-input", min=-180, step=0.01, value=12, style={"width": "100%"})
                        ], style={"width": "48%", "display": "inline-block", "marginRight": "4%"}),

                        html.Div([
                            html.Label("Latitude", style={"fontWeight": "bold"}),
                            dcc.Input(type="number", id="lat-input", min=-90, step=0.01, value=12, style={"width": "100%"})
                        ], style={"width": "48%", "display": "inline-block"})
                    ]),
                    html.Br(),

                    html.Label("Number of Vehicles Involved", style={"fontWeight": "bold"}),
                    dcc.Input(type="number", id="vehicles-input", min=1, step=1, value=12, style={"width": "100%"}),
                    html.Br(), html.Br(),

                    html.Label("Select Weather Condition", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        options=[{'label': c, 'value': c} for c in sorted(accidents_df['Weather Condition'].unique())],
                        id="weather-dropdown"
                    ),
                    html.Br(),

                    html.Label("Select Road Condition", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        options=[{'label': c, 'value': c} for c in sorted(accidents_df['Road Condition'].unique())],
                        id="road-dropdown"
                    ),
                    html.Br(),

                    html.Label("Select Cause", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        options=[{'label': c, 'value': c} for c in sorted(accidents_df['Cause'].unique())],
                        id="cause-dropdown"
                    ),
                    html.Br(),

                    html.Div([
                        html.Div([
                            html.Label("Select Date", style={"fontWeight": "bold"}),
                            dcc.DatePickerSingle(
                                id="date-picker",
                                date=accidents_df['Date'].max(),
                                style={"width": "100%"}
                            )
                        ], style={"width": "48%", "display": "inline-block", "marginRight": "4%"}),

                        html.Div([
                            html.Label("Select Time", style={"fontWeight": "bold"}),
                            dmc.TimeInput(
                                id="hour-input",
                                withSeconds=False,
                                style={"width": "100%"}
                            )
                        ], style={"width": "48%", "display": "inline-block"})
                    ]),

                    html.Br(),

                    html.Div([
                        html.Button("Assess", id="submit-assess-btn", n_clicks=0, style={
                            "backgroundColor": "#28a745",
                            "color": "white",
                            "border": "none",
                            "padding": "10px 24px",
                            "textAlign": "center",
                            "textDecoration": "none",
                            "display": "inline-block",
                            "fontSize": "16px",
                            "borderRadius": "6px",
                            "cursor": "pointer",
                            "width": "100%"
                        }),
                    
                        html.Br(),

                        html.Div(
                            id="prediction-output",
                            style={
                                "marginTop": "10px",
                                "padding": "15px",
                                "border": "1px solid #ccc",
                                "borderRadius": "8px",
                                "backgroundColor": "#f9f9f9",
                                "fontSize": "18px",
                                "fontWeight": "bold",
                                "color": "#155724",
                                "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.1)"
                            }
                        )
                    ])
                ], style={"padding": "20px", "fontFamily": "Arial, sans-serif"})
            ], width=4)
        ])
    
    else:
        return html.Div("No content available")


@callback(
    Output("main-forecast-graph", "figure", allow_duplicate=True),
    Output("forecast-card-title", "children", allow_duplicate=True),
    Output('city-dropdown', 'options'),
    Input('country-dropdown', 'value'),
    prevent_initial_call=True
)
def update_city_dropdown(selected_country):
    
    cities_menu = []
    title = "Global Monthly Average Casualties" 
    fig = monthly_casualties(accidents_df, '')

    city_country_map = {
                        'Australia': ['Sydney'],
                        'Brazil': ['São Paulo'],
                        'Canada': ['Toronto'],
                        'China': ['Beijing'],  
                        'France': ['Paris'],
                        'Germany': ['Berlin'],
                        'India': ['Mumbai'],
                        'Japan': ['Tokyo'],
                        'UK': ['London'],
                        'USA': ['New York']
                      }
    
    if not selected_country:
        return fig, title, cities_menu
    
    elif selected_country.strip() in city_country_map:
        title = f"{selected_country.strip()} Monthly Average Casualties" 
        fig = monthly_casualties(accidents_df, selected_country.strip())
        cities_menu = city_country_map[selected_country.strip()]
    
    return fig, title, cities_menu


@callback(
    Output("prediction-output", "children"),
    Input("submit-assess-btn", "n_clicks"),
    State("country-dropdown", "value"),
    State("city-dropdown", "value"),
    State("lat-input", "value"),
    State("long-input", "value"),
    State("vehicles-input", "value"),
    State("weather-dropdown", "value"),
    State("road-dropdown", "value"),
    State("cause-dropdown", "value"),
    State("date-picker", "date"),
    State("hour-input", "value"),
    prevent_initial_call=True
)
def predict_casualties(n_clicks, country, city, lat, lon, vehicles, weather, road, cause, date, hour):

    if not date:
        return "Please select a date."

    # Parse date
    date_obj = datetime.datetime.strptime(date[:10], "%Y-%m-%d")
    year, month, day = date_obj.year, date_obj.month, date_obj.day
    day_of_week = date_obj.weekday()  # Monday = 0

    # Cast hour
    hour = pd.to_datetime(hour, format='%H:%M').hour

    # Base data
    input_data = {
                    'Year': year,
                    'Month': month,
                    'Day': day,
                    'DayOfWeek': day_of_week,
                    'Hour': hour,
                    'Latitude': lat,
                    'Longitude': lon,
                    'Vehicles Involved': vehicles
                }

    # One-hot encode city
    for col in assessment_feature_columns:
        if col.startswith("City_"):
            input_data[col] = 1 if col == f"City_{city}" else 0

    # One-hot encode country
    for col in assessment_feature_columns:
        if col.startswith("Country_"):
            input_data[col] = 1 if col == f"Country_{country}" else 0  # Fixed space issue

    # One-hot encode weather
    for col in assessment_feature_columns:
        if col.startswith("Weather Condition_"):
            input_data[col] = 1 if col == f"Weather Condition_{weather}" else 0

    # One-hot encode road
    for col in assessment_feature_columns:
        if col.startswith("Road Condition_"):
            input_data[col] = 1 if col == f"Road Condition_{road}" else 0

    # One-hot encode cause
    for col in assessment_feature_columns:
        if col.startswith("Cause_"):
            input_data[col] = 1 if col == f"Cause_{cause}" else 0

    # Convert to DataFrame
    df_input = pd.DataFrame([input_data])
    df_input = df_input.reindex(columns=assessment_feature_columns, fill_value=0)

    # Predict
    try:
        prediction = assessment_model.predict(df_input)[0]
        return f"Predicted Casualties: {int(prediction)}"
    
    except Exception as e:
        return f"Error during prediction: {str(e)}"


@callback(
    Output("main-forecast-graph", "figure", allow_duplicate=True),
    Input("month-slider", "value"),
    State("model-dropdown", "value"),
    prevent_initial_call=True
)
def generate_forecast(months, model_type):

    if model_type == "forecast_accidents":
        monthly_counts, last_known = get_accidents_features(accidents_df)
        future_dates, future_predictions = forecast_interval(accidents_forecast_model, monthly_counts, months, last_known)
        x_col, y_col = monthly_counts['YearMonth'], monthly_counts['AccidentsCount']
        title = 'Accidents'

    elif model_type == "forecast_casualties":
        monthly_counts, last_known = get_casualties_features(accidents_df)
        future_dates, future_predictions = forecast_interval(casualties_forecast_model, monthly_counts, months, last_known)
        x_col, y_col = monthly_counts['YearMonth'], monthly_counts['Casualties']
        title = 'Casualties'

    else:
        return go.Figure().update_layout(title="Invalid Model Selection")

    # Plotting forecast
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_col, y=y_col, mode='lines+markers', line=dict(color='#001f3f'), marker=dict(color='#001f3f'),  name='Historical'))
    fig.add_trace(go.Scatter(x=future_dates, y=future_predictions, mode='lines+markers', name='Forecast'))

    # Add dashed connector between last historical and first forecasted point
    if len(x_col) > 0 and len(future_dates) > 0:
        fig.add_trace(go.Scatter(
                                    x=[x_col.iloc[-1], future_dates[0]],
                                    y=[y_col.iloc[-1], future_predictions[0]],
                                    mode='lines',
                                    line=dict(color='#001f3f', dash='dash'),
                                    showlegend=False
                                ))

    fig.update_layout(title='', xaxis_title='Date', yaxis_title=title, template='plotly_white')

    return fig