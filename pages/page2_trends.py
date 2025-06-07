import dash_bootstrap_components as dbc 
from dash import html, dcc, Input, Output, callback
import plotly.express as px 
from data import data_preprocess


# -------------------------------------------------- Trends & insights layout -------------------------------------------------- #
accidents_df=data_preprocess('dataset\global_traffic_accidents.csv')
header_trends=html.Div([
        html.H2("🚗 Accident Characteristics & Trends", className="mt-4"),
        html.P("Deep dive into temporal patterns, environmental factors, and accident severity analysis", 
               className="lead"),
    ], className="text-center mb-4"),





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
       
trends_layout = html.Div([
    html.Div([
            dbc.Card([
                html.H5("Accident Trends Over Time", className="card-title text-center mt-3"),
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
          dbc.Card([
            html.Div(id='env-title', className="card-title text-center mt-3"),
            dcc.Dropdown(
                id='env-dropdown',
                options=[
                    {'label': 'Weather Condition', 'value': 'Weather Condition'},
                    {'label': 'Road Condition', 'value': 'Road Condition'},
                     {'label': 'Cause of accidents', 'value': 'Cause'},
                ],
                value='Weather Condition',
                clearable=False,
                style={"margin": "10px"}
            ),
            dcc.Graph(id='env-boxplot')
        ], className="mb-4 p-3",style={"border": "1px solid #001f3f","borderRadius": "20px","margin-left":"80px","margin-bottom":"20px",}),
       
        dbc.Row(children=[
        dbc.Card([
           html.H5("Accident Severity (Based on Casualties & Vehicles)", className="card-title text-center mt-3"),
            dcc.Graph(figure=create_severity_figure())
        ], className="mb-4 p-3",style={"border": "1px solid #001f3f","borderRadius": "20px","margin-left":"80px","margin-bottom":"20px","width":"1100px"}),
       
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
    # Count number of accidents per category
    grouped_df = accidents_df[selected_feature].value_counts().reset_index()
    grouped_df.columns = [selected_feature, 'Number of Accidents']

    # Create bar chart
    fig = px.bar(
    grouped_df,
    x=selected_feature,
    y='Number of Accidents',
    color=selected_feature,  # this is the key part!
    color_discrete_sequence=['#1e2d3b', '#36454f', '#3e78b2', '#003366', '#001f3f','#3a6d8c'],
    labels={'Number of Accidents': 'Number of Accidents'}
     )
    fig.update_layout(showlegend=False)
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
    return html.H5(feature_map.get(selected_feature, "Accident Analysis"), className="mt-3")
