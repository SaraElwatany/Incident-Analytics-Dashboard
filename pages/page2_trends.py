import dash_bootstrap_components as dbc 
from dash import html, dcc, Input, Output, callback
from dash_bootstrap_components._components.Col import Col
import plotly.express as px 
from data import data_preprocess
import pandas as pd

accidents_df=data_preprocess('dataset\global_traffic_accidents.csv')

header_trends=html.Div([
        html.H2("🚗 Accident Characteristics & Trends", className="mt-4"),
        html.P("Deep dive into temporal patterns, environmental factors, and accident severity analysis", 
               className="lead"),
    ], className="text-center mb-4"),



# ---------- Global Styles ----------
styles = {
    "card": {
        "border": "1px solid #001f3f",
        "borderRadius": "20px",
        "margin-left": "80px",
        "margin-bottom": "20px",
        "padding": "1rem"
    },
    "card_title": {
        "fontWeight": "bold"
    },
    "tab": {
        'border': '2px solid #001f3f',
        'border-radius': "25px",
        'padding': '10px',
        'fontWeight': 'bold',
        'width': '200px',
        'margin': '5px',
    },
    "datepicker": {
        "borderRadius": "25px",
        "margin": "10px",
        "color": "#001f3f"
    }
}




# === Figure Generators ===

def create_accidents_over_date(selected_metric):
    monthly_data = accidents_df.groupby(['Year','Month_Num'])[selected_metric].sum().reset_index()
    pivot_df = monthly_data.pivot(index='Month_Num', columns='Year', values=selected_metric).reset_index()
    pivot_df['Month'] = pivot_df['Month_Num'].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%b'))
    pivot_df = pivot_df.sort_values('Month_Num')
    fig = px.line(pivot_df,
                x='Month',
                y=[pivot_df.columns[1], pivot_df.columns[2]],   
                markers=True,
                labels={"value": selected_metric, "variable": "Year"},
                template='plotly_white',    
                color_discrete_sequence=["#001f3f", "#800020"]
    )
    return fig

def create_severity_figure():
    severity_counts = accidents_df['Severity'].value_counts().reset_index()
    severity_counts.columns = ['Severity', 'Count']
    fig = px.pie(
        severity_counts,
        names='Severity',
        values='Count',
        color='Severity',
        color_discrete_map={
            'Minor': '#36454f',
            'Moderate': '#001f3f',
            'Severe': '#800020'
        }
    )
    return fig

def create_accidents_with_time():
    weather_mode = accidents_df.groupby('Time Segment')['Weather Condition'].agg(lambda x: x.mode().iloc[0])
    road_mode = accidents_df.groupby('Time Segment')['Road Condition'].agg(lambda x: x.mode().iloc[0])
    segment_counts = accidents_df['Time Segment'].value_counts().reset_index()
    segment_counts.columns = ['Time Segment', 'Count']
    segment_counts['Weather Condition'] = segment_counts['Time Segment'].map(weather_mode)
    segment_counts['Road Condition'] = segment_counts['Time Segment'].map(road_mode)
    segment_counts['Hover'] = (
        'Time Segment: ' + segment_counts['Time Segment'] +
        '<br>Accidents: ' + segment_counts['Count'].astype(str) +
        '<br>Common Weather: ' + segment_counts['Weather Condition'] +
        '<br>Common Road: ' + segment_counts['Road Condition']
    )

    fig = px.pie(
    segment_counts,
    names='Time Segment',
    values='Count',
    template='plotly_white',    
    color_discrete_sequence=["#000000","#bfad85","#003366","#001f3f"],
    hover_data=['Hover'] 
    )
    fig.update_traces(
    hovertemplate='%{customdata[0]}<extra></extra>'
    )
    return fig

# === Layout ===
       
trends_layout = html.Div([
    html.Div([
            dbc.Card([
                html.H5("Accident Trends Over Time",
                       className="card-title text-center mt-3",
                       style=styles["card_title"]
                    ),
                 dcc.DatePickerRange(   
                    id='date-range',
                    start_date=accidents_df['Date'].min(),
                    end_date=accidents_df['Date'].max(),
                    min_date_allowed=accidents_df['Date'].min(),
                    max_date_allowed=accidents_df['Date'].max(),
                    display_format='YYYY-MM-DD',
                    style=styles["datepicker"]
                ),
                
                dcc.Graph(id='time-series'),
            ],
             className="mb-4 p-3",
             style=styles["card"]
            ),
          
          dbc.Card([
                html.Div(id='env-title',
                        className="card-title text-center mt-3"
                    ),
                dcc.Dropdown(
                    id='env-dropdown',
                    options=[
                        {'label': 'Weather Condition', 'value': 'Weather Condition'},
                        {'label': 'Road Condition', 'value': 'Road Condition'},
                        {'label': 'Cause of accidents', 'value': 'Cause'},
                    ],
                    value='Weather Condition',
                    style={
                        "margin": "10px",
                    }
                ),
                dcc.Graph(id='env-boxplot')
            ],
             className="mb-4 p-3",
             style=styles["card"]
            ),
        
         dbc.Card([
            html.H5("Casualties in 2023 vs Casualties in 2024 Monthly Trend",
                    className="card-title text-center mt-3",
                    style=styles["card_title"]
                ),
                dcc.Tabs(
                    id='metric-selector',
                    value='Casualties',
                    children=[
                        dcc.Tab(
                            label='Casualties',
                            value='Casualties', 
                            style=styles["tab"],
                            selected_style=styles["tab"]
                        ),
                        dcc.Tab(
                            label='Vehicles Involved',
                            value='Vehicles Involved', 
                            style=styles["tab"],
                            selected_style=styles["tab"]
                        ),
                    ],
                ),

                dcc.Graph(id='monthly-trend-graph')
            ],
             className="mb-4 p-3",
             style=styles["card"]
            ),
        
        dbc.Row(children=[
            dbc.Col([
                dbc.Card([
                    html.H5("Accident Severity (Based on Casualties & Vehicles)",
                            className="card-title text-center mt-3",
                            style=styles["card_title"]
                        ),
                        dcc.Graph(figure=create_severity_figure()
                    ),
                ],
                 className="mb-4 p-3",
                 style=styles["card"]
                ),  
            ]),

            dbc.Col([
               dbc.Card([
                    html.H5("Accidents by Time of Day",
                            className="card-title text-center mt-3",
                            style=styles["card_title"]
                    ),
                   dcc.Graph(figure=create_accidents_with_time())
                ], 
                 className="mb-4 p-3",
                 style=styles["card"]
                ),
            ]),
        ]),  
    ])
])

# === Callbacks ===

@callback(
    Output('time-series', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_time_series(start_date, end_date):
    mask = (accidents_df['Date'] >= start_date) & (accidents_df['Date'] <= end_date)
    filtered_data = accidents_df.loc[mask]
    grouped = filtered_data.groupby('Date').size().reset_index(name='accident_count')
    fig = px.line(
              grouped, 
              x='Date',
              y='accident_count',
              labels={'accident_count': 'Number of Accidents'},
              template='plotly_white',
              color_discrete_sequence=['#001f3f']
            )
    fig.update_traces(mode='lines+markers')
    return fig

@callback(
    Output('env-boxplot', 'figure'),
    Input('env-dropdown', 'value')
)
def update_env_plot(selected_feature):
    grouped_df = accidents_df.groupby(selected_feature).agg({
        'Casualties': 'sum',
        selected_feature: 'count',
        'Vehicles Involved': 'sum',
    }).rename(columns={
        selected_feature: 'Number of Accidents',
        'Casualties': 'Total Casualties',
        'Vehicles Involved': 'Total Vehicles',
    }).reset_index()
    grouped_df['Hover'] = grouped_df.apply(lambda row: (
        f"{selected_feature}: {row[selected_feature]}"
        f"<br>Number of Accidents: {row['Number of Accidents']}"
        f"<br>Total Casualties: {row['Total Casualties']}"
        f"<br>Total Vehicles: {row['Total Vehicles']}"
    ), axis=1)
    fig = px.bar(
        grouped_df,
        x=selected_feature,
        y='Number of Accidents',
        template='plotly_white',
        color=selected_feature,
        color_discrete_sequence=['#1e2d3b', '#36454f', '#3e78b2', '#003366', '#001f3f','#3a6d8c'],
        hover_data=['Hover']
    )

    fig.update_traces(
        hovertemplate='%{customdata[0]}<extra></extra>'
    )
    return fig

@callback(
    Output('env-title', 'children'),
    Input('env-dropdown', 'value')
)
def update_env_title(selected_feature):
    feature_map = {
        "Weather Condition": "Accidents by Weather Condition",
        "Road Condition": "Accidents by Road Condition",
        "Cause": "Accidents by Cause"
    }
    return html.H5(feature_map.get(selected_feature, "Accident Analysis"), className="mt-3",style={'fontWeight': 'bold'})


@callback(
    Output('monthly-trend-graph', 'figure'),
    Input('metric-selector', 'value')
)
def update_trend_graph(selected_metric):
    fig=create_accidents_over_date(selected_metric)
    return fig

