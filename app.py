import datetime
from dash_bootstrap_components._components.Card import Card
from dash_bootstrap_components._components.Row import Row
import numpy as np 
import pandas as pd 
from joblib import load        
import plotly.express as px  

# Dash  
import plotly.graph_objects as go
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc 
from dash import Dash, html, dcc, Input, Output, State, callback

# User-Defined Modules
from graphs import monthly_casualties
  




# Global Variables
accidents_df = pd.read_csv('dataset/global_traffic_accidents.csv')
accidents_df['City'] = accidents_df['Location'].map(lambda x:x.split(',')[0])
accidents_df['Country'] = accidents_df['Location'].map(lambda x:x.split(',')[1])
accidents_df['Date'] = pd.to_datetime(accidents_df['Date'])
accidents_df['Time']=pd.to_datetime(accidents_df['Time'],format='%H:%M').dt.time


assessment_feature_columns = load(open('models/assessment_feature_columns.pkl', 'rb'))


assessment_model = load('models/assessment_model.pkl')
#casualties_forecast_model = load('models/casualties_forecast_model.pkl')
#accidents_forecast_model = load('models/accidents_forecast_model.pkl')


# Initialize the dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO], suppress_callback_exceptions=True)
server = app.server



# ----------------- Application Layouts ----------------- #



# Sidebar Style
sidebar_style = {
                    "position": "fixed",
                    "width": "20rem",
                    "height": "100vh",
                    "top": "0",
                    "bottom": "0",
                    "left": "0",
                    "padding": "20px",
                    "background-color": "#001f3f",  # Navy Blue
                    "font-family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",  # Change font
                    "font-size": "25px",  # Adjust size as needed
                    "font-weight": "500",  # Optional: 400 = normal, 700 = bold
                    "color": "#FFD700",  # Yellow text
                }


# Page Content Style
content_style = {
                    "margin-left": "16rem",
                    "margin-right": "0rem",
                    "padding": "30px",
                    "height": "100%",
                    "background-color": "#f3f3f3",  # Light Grey
                }



# Pages Navigator
pages_dict = {
                "Home" : "/",
                "Trends": "/trends",
                "Experiences": "/experinces",
                "Forecast Accidents": "/TimeSeries"
            }



# Nav Bar
sidebar = html.Div(

    [
        html.Div([
                    html.H2([
                        html.Img(
                            src="https://img.icons8.com/ios-filled/100/FFD700/globe-earth.png",  # Yellow globe icon
                            style={
                                'height': '50px',
                                'margin-right': '10px',
                                'borderRadius': '50%',
                                'background-color': '#001f3f',  # Navy background for contrast
                                'padding': '5px'
                            }
                        ),
                        "Incidentlytics"
                    ], style={
                        'display': 'flex',
                        'align-items': 'center',
                        'font-size': '28px',
                        'font-weight': '700',
                        'color': 'white',  # white text
                        'font-family': 'Segoe UI, sans-serif',
                        'margin-bottom': '20px'
                    })
                ]),
        
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        
        dbc.Nav(
            [
                dbc.NavLink(k, href=f"{v}",
                            className="btn", active="exact",
                            style={
                                    "margin-bottom": "15px",
                                    "background-color": "#001f3f",  # Match sidebar bg
                                    "color": "#FFD700",  # Yellow text
                                    "font-weight": "600",
                                    "border": "1px solid #FFD700",
                                    "border-radius": "5px",
                                    "padding": "10px",
                                })
                for k, v in pages_dict.items()
            ],
            vertical=True,
            pills=True,
        ),




    ],
    style=sidebar_style
)


# Application Header
header =  html.H1(f"", id="header", style={"text-align":"center"})


# page content
content = html.Div(id="page-content", children = [], style = content_style)


# App Layout
app.layout = dmc.MantineProvider(
                                    children=[
                                        html.Div([
                                                    dcc.Location(id="page-url"),
                                                    sidebar,
                                                    header,
                                                    content,
                                                ], className="container-fluid")
                                    ]
                                )




# -------------------------------------------------- Pages Layouts -------------------------------------------------- #

home_layout = html.Div([
    html.H2("Welcome to the Home Page"),
    html.P("This is the overview of the Incidentlytics Dashboard.")
])


# -------------------------------------------------- Trends & insights layout -------------------------------------------------- #
header_trends=html.Div([
        html.H2("🚗 Accident Characteristics & Trends", className="mt-4"),
        html.P("Deep dive into temporal patterns, environmental factors, and accident severity analysis", 
               className="lead"),
    ], className="text-center mb-4"),

        
trends_layout = html.Div([
    html.Div([
        dbc.Row(children=[
            dbc.Card([
                 dcc.DatePickerRange(   
                    id='date-range',
                    start_date=accidents_df['Date'].min(),
                    end_date=accidents_df['Date'].max(),
                    min_date_allowed=accidents_df['Date'].min(),
                    max_date_allowed=accidents_df['Date'].max(),
                    display_format='YYYY-MM-DD',
                    style={
                          
                        "borderRadius": "2px",
                        "margin":"10px",
                        "color": "#001f3f"                   
                    }
                ),
                
                dcc.Graph(id='time-series'),
            ],className="mb-4 p-3",style={"border": "1px solid #001f3f","borderRadius": "20px","margin-left":"80px","margin-bottom":"20px","width":"1100px"}),
        ]),
        dbc.Col([
            dbc.Card([
            html.H5("Casualties by Environment", className="card-title text-center mt-3"),
            dcc.Dropdown(
                id='env-dropdown',
                options=[
                    {'label': 'Weather Condition', 'value': 'Weather Condition'},
                    {'label': 'Road Condition', 'value': 'Road Condition'}
                ],
                value='Weather Condition',
                clearable=False,
                style={"margin": "10px"}
            ),
            dcc.Graph(id='env-boxplot')
        ], className="mb-4 p-3",style={"border": "1px solid #001f3f","borderRadius": "20px","margin-left":"80px","margin-bottom":"20px",}),
           
        ]), 
    ])
])

@callback(
    Output('time-series', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_time_series(start_date, end_date):
    # Filter dataset
    mask = (accidents_df['Date'] >= start_date) & (accidents_df['Date'] <= end_date)
    filtered_data = accidents_df.loc[mask]

    # Group by date
    grouped = filtered_data.groupby('Date').size().reset_index(name='accident_count')

    # Create figure
    fig = px.line(grouped, x='Date', y='accident_count',
                  title='Accident Trends Over Time',
                  labels={'accident_count': 'Number of Accidents'},
                  template='plotly_white')
    fig.update_traces(mode='lines+markers')
    return fig

@callback(
    Output('env-boxplot', 'figure'),
    Input('env-dropdown', 'value')
)
def update_env_plot(selected_feature):
    # Count number of accidents per category
    grouped_df = accidents_df[selected_feature].value_counts().reset_index()
    grouped_df.columns = [selected_feature, 'Number of Accidents']

    # Create bar chart
    fig = px.bar(
        grouped_df,
        x=selected_feature,
        y='Number of Accidents',
         
        labels={'Number of Accidents': 'Number of Accidents'},


    )
    fig.update_layout(showlegend=False)
    return fig


#------------------------------------------------------------------------------------------
experiences_layout = html.Div([
    html.H2("Experiences Page"),
    html.P("This page contains user experiences or analysis.")
])














# -------------------------------------------------- Forecasting Page Layout -------------------------------------------------- #

forecast_layout = html.Div([

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

    # Row with left and right sections
    dbc.Row([

        # Left: Large graph
        dbc.Col(
            dcc.Graph(id="main-forecast-graph"),
            width=8
        ),

        # Right: Dynamic content (inputs or smaller graphs)
        dbc.Col(
            html.Div(id="right-column"),
            width=4
        )

    ])

], style={"padding": "70px"})









@app.callback(
    Output("main-forecast-graph", "figure"),
    Output("right-column", "children"),
    Input("model-dropdown", "value")
)
def update_forecast_layout(selected_model):

    if selected_model == "forecast_casualties":
        fig = monthly_casualties(accidents_df)
        right_content = html.Div([
            dcc.Graph(id="secondary-graph-1", figure=go.Figure().update_layout(title="Placeholder 1")),
            html.Br(),
            dcc.Graph(id="secondary-graph-2", figure=go.Figure().update_layout(title="Placeholder 2"))
        ])
        return fig, right_content

    elif selected_model == "assess_accident":

        fig = monthly_casualties(accidents_df)

        #
        right_content = html.Div([
                                    html.H4("Accident Assessment Inputs", style={"fontWeight": "bold", "marginBottom": "20px"}),

                                    html.Label("Select City", style={"fontWeight": "bold"}),
                                    dcc.Dropdown(
                                        options=[{'label': c, 'value': c} for c in sorted(accidents_df['City'].unique())],
                                        id="city-dropdown"
                                    ),
                                    html.Br(),

                                    html.Label("Select Country", style={"fontWeight": "bold"}),
                                    dcc.Dropdown(
                                        options=[{'label': c, 'value': c} for c in sorted(accidents_df['Country'].unique())],
                                        id="country-dropdown"
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
                                    html.Br(), html.Br(),

                                    html.Div(id="prediction-output", style={"marginTop": "20px", "fontSize": "20px", "color": "darkgreen", "fontWeight": "bold"}),

                                    html.Div([
                                        html.Button("Assess", id="submit-assess-btn", n_clicks=0, style={
                                            "backgroundColor": "#007BFF",
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
                                        })
                                    ])
                                ], style={"padding": "20px", "fontFamily": "Arial, sans-serif"})

        return fig, right_content

    else:
        return go.Figure().update_layout(title="No Data"), html.Div()





@app.callback(
    Output("prediction-output", "children"),
    Input("submit-assess-btn", "n_clicks"),
    State("city-dropdown", "value"),
    State("country-dropdown", "value"),
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
def predict_casualties(n_clicks, city, country, lat, lon, vehicles, weather, road, cause, date, hour):

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
            input_data[col] = 1 if col == f"Country_ {country}" else 0

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






@app.callback(
    Output("page-content", "children"),
    Output("header", "children"),
    Input("page-url", "pathname")
)
def display_page(pathname):
    if pathname == "/":
        return home_layout, "Home"
    elif pathname == "/trends":
        return trends_layout,header_trends 
    elif pathname == "/experinces":
        return experiences_layout, "Experiences"
    elif pathname == "/TimeSeries":
        return forecast_layout, "Forecast Accidents"
    else:
        return html.Div([html.H2("404 - Page Not Found")]), "Not Found"
























# # ---------------- Home Page Graphs ----------------

# def create_top_job_chart(year):

#     if year == "all":
#         df_filtered = df.copy()

#     else:
#         filt = df["Year"] == year  # df[df["Year"] == year]
#         df_filtered = df[filt].copy()

#     df_filtered = df_filtered["Job_Title"].value_counts().sort_values(ascending=False).head(10)[::-1]

#     # Bar Chart of Wanted Job
#     fig_wanted_job = px.bar(df_filtered,
#                  orientation="h",
#                  y = df_filtered.index ,
#                  x = (df_filtered / sum(df_filtered)) * 100,
#                  # color = df_filtered.index,
#                  color_discrete_sequence=["#90CAF9"],
#                  title= "Top Demanded Job",
#                  labels={"x": "Popularity of Jobs(%)", "Job_Title": "Job Title"},
#                  template="plotly",
#                  text = df_filtered.apply(lambda x: f"{(x / sum(df_filtered)) * 100:0.2f}%")
#                  )

#     fig_wanted_job.update_layout(
#         showlegend= False,
#         title={
#             "font": {
#                 "size": 35,
#                 "family": "tahoma",
#             }
#         }
#     )

#     fig_wanted_job.update_traces(
#         textfont = {
#                    "family": "consolas",
#                    "size": 14,
#                     "color":"white"
#                    },
#         hovertemplate="Job Title: %{label}<br>Popularity (%): %{value}",
#     )

#     return fig_wanted_job



# def create_cards(year):

#     if year == "all":
#         df_filtered = df.copy()
#     else:
#         filt = df["Year"] == year
#         df_filtered = df[filt].copy()

#     all_jobs = df_filtered["Job_Title"].nunique()
#     avg_salary = df_filtered["Salary_in_USD"].mean()
#     avg_salary = f"${avg_salary:0,.0f}"


#     return [all_jobs, avg_salary]














if __name__ == "__main__":
    app.run(debug=True)