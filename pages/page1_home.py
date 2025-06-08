import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import sys
import os
from data import data_preprocess

# Load and preprocess data globally 
df = data_preprocess('dataset/global_traffic_accidents.csv')

color_seq = [
    "#b0c4de",  
    "#3a6d8c",
    "#3e78b2",
    "#36454f",
    "#003366",
    "#001f3f"    
]

def create_insights_layout():
    layout = html.Div([
        dbc.Card([
            dbc.Row([
                dbc.Col([
                    html.Label("Select Date Range"),
                    dcc.DatePickerRange(
                        id='date-picker',
                        start_date=df['Date'].min(),
                        end_date=df['Date'].max(),
                        min_date_allowed=df['Date'].min(),
                        max_date_allowed=df['Date'].max(),
                        display_format='YYYY-MM-DD',
                        style={"margin": "10px", "width": "100%"}
                    )
                ], width=4),
                dbc.Col([
                    html.Label("Select Country"),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': c, 'value': c} for c in sorted(df['Country'].unique())],
                        multi=True,
                        style={"width": "100%"}
                    )
                ], width=4),
                dbc.Col([
                    html.Label("Select Weather Condition"),
                    dcc.Dropdown(
                        id='weather-dropdown',
                        options=[{'label': w, 'value': w} for w in sorted(df['Weather Condition'].unique())],
                        multi=True,
                        style={"width": "100%"}
                    )
                ], width=4),
            ], className="mb-4", style={"padding": "10px"}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H5("Accident Density by Country", className="card-title text-center mt-3",
                                style={'fontWeight': 'bold'}),
                        dcc.Graph(id='choropleth-map')
                    ], className="mb-4 p-3", style={"border": "1px solid #001f3f", "borderRadius": "20px"})
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H5("Top Cities with Most Accidents", className="card-title text-center mt-3",
                                style={'fontWeight': 'bold'}),
                        dcc.Graph(id='bar-chart')
                    ], className="mb-4 p-3", style={"border": "1px solid #001f3f", "borderRadius": "20px"})
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        html.H5("Weather × Road Conditions During Accidents", className="card-title text-center mt-3",
                                style={'fontWeight': 'bold'}),
                        dcc.Graph(id='sunburst-chart')
                    ], className="mb-4 p-3", style={"border": "1px solid #001f3f", "borderRadius": "20px"})
                ], width=6)
            ])
        ], className="mb-4 p-3", style={"border": "1px solid #001f3f", "borderRadius": "20px", "margin-left": "80px", "width": "1110px"})
    ])
    return layout

def filter_data(start_date, end_date, selected_countries, selected_weather):
    filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    if selected_weather:
        filtered = filtered[filtered['Weather Condition'].isin(selected_weather)]
    if selected_countries:
        filtered = filtered[filtered['Country'].isin(selected_countries)]
    return filtered

@callback(
    Output('choropleth-map', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('country-dropdown', 'value'),
    Input('weather-dropdown', 'value'),
)
def update_choropleth(start_date, end_date, selected_countries, selected_weather):
    filtered_df = filter_data(start_date, end_date, selected_countries, selected_weather)
    if selected_countries and len(selected_countries) == 1:
        country_name = selected_countries[0]
        city_counts = (
            filtered_df.groupby('Location')
            .size()
            .reset_index(name='Accident Count')
            .sort_values('Accident Count', ascending=False)
            .head(10)
        )
        fig = px.scatter_geo(
            city_counts,
            locations='Location',
            locationmode='country names',
            color='Accident Count',
            size='Accident Count',
            hover_name='Location',
            projection='natural earth',
            title=f'Accident Locations in {country_name}',
            color_continuous_scale=color_seq,
            size_max=20,
            height=500,
        )
        fig.update_geos(
            fitbounds="locations",
            showcountries=True,
            countrycolor="Black",
            visible=True,
            resolution=50,
        )
    else:
        accident_counts = (
            filtered_df.groupby('Country')
            .size()
            .reset_index(name='Accident Count')
        )
        fig = px.choropleth(
            accident_counts,
            locations='Country',
            locationmode='country names',
            color='Accident Count',
            color_continuous_scale=color_seq,
            title="Accident Density by Country",
            height=500,
        )
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

@callback(
    Output('bar-chart', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('country-dropdown', 'value'),
    Input('weather-dropdown', 'value'),
)
def update_bar_chart(start_date, end_date, selected_countries, selected_weather):
    filtered_df = filter_data(start_date, end_date, selected_countries, selected_weather)
    top_cities = (
        filtered_df['Location']
        .value_counts()
        .head(5)
        .reset_index(name='Accident Count')
    )
    top_cities.rename(columns={'index': 'Location'}, inplace=True)
    fig = px.bar(
        top_cities.sort_values('Accident Count', ascending=False),
        x='Location',
        y='Accident Count',
        color='Accident Count',
        color_continuous_scale=color_seq,
        template='plotly_white',
        text='Accident Count'
    )
    fig.update_traces(
        textposition='outside',
        marker_line_color='#36454f',
        marker_line_width=1.5
    )
    fig.update_layout(
        xaxis_title='City',
        yaxis_title='Number of Accidents',
        coloraxis_showscale=False,
        plot_bgcolor='#f7f9fa',
        margin=dict(l=60, r=20, t=60, b=40)
    )
    return fig

@callback(
    Output('sunburst-chart', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('country-dropdown', 'value'),
    Input('weather-dropdown', 'value'),
)
def update_pie_chart(start_date, end_date, selected_countries, selected_weather):
    filtered_df = filter_data(start_date, end_date, selected_countries, selected_weather)
    combo_counts = (
        filtered_df.groupby(['Weather Condition', 'Road Condition'])
        .size()
        .reset_index(name='Count')
        .sort_values('Count', ascending=False)
        .head(5)
    )
    combo_counts['Label'] = combo_counts['Weather Condition'] + " / " + combo_counts['Road Condition']
    fig = px.pie(
        combo_counts,
        names='Label',
        values='Count',
        color_discrete_sequence=color_seq
    )
    fig.update_traces(textinfo='percent+label', pull=[0.05]*len(combo_counts))
    default_start = df['Date'].min().strftime("%Y-%m-%d")
    default_end = df['Date'].max().strftime("%Y-%m-%d")
    if start_date is None:
        start_date = default_start
    if end_date is None:
        end_date = default_end
    start_date_short = start_date[:10]
    end_date_short = end_date[:10]
    date_filtered = (start_date_short != default_start) or (end_date_short != default_end)
    filters_applied = (
        selected_weather or
        selected_countries or
        date_filtered
    )
    show_legend = not filters_applied
    fig.update_layout(
        showlegend=show_legend,
        legend=dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.05
        ),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig
