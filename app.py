import dash_mantine_components as dmc
import dash_bootstrap_components as dbc 
from dash import Dash, html, dcc, Input, Output

# User-Defined Modules
from pages.page1_home import create_insights_layout 
from pages.page2_trends import trends_layout  
from pages.page3_forecast import create_forecast_layout 

# Initialize the dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO], suppress_callback_exceptions=True)
server = app.server

# ----------------- Application Layouts ----------------- #

# Top Navigation Bar Style
navbar_style = {
    "position": "fixed",
    "top": "0",
    "left": "0",
    "right": "0",
    "height": "80px",
    "background-color": "#001f3f",  # Navy Blue
    "z-index": "1000",
    "padding": "10px 20px",
    "box-shadow": "0 2px 10px rgba(0,0,0,0.1)"
}

# Sidebar Style (for filters)
sidebar_style = {
    "position": "fixed",
    "width": "22rem",
    "height": "100vh",
    "top": "80px",  # Below navbar
    "bottom": "0",
    "left": "0",
    "padding": "20px",
    "background-color": "#f8f9fa",  # Light background
    "border-right": "2px solid #001f3f",
    "overflow-y": "auto",
    "z-index": "999"
}

# Page Content Style
content_style = {
    "margin-left": "22rem",  # Space for sidebar
    "margin-top": "80px",    # Space for navbar
    "padding": "30px",
    "min-height": "calc(100vh - 80px)",
    "background-color": "#f3f3f3",
}

# Pages Navigator
pages_dict = {
    "Home": "/",
    "Trends": "/trends",
    "Forecast Accidents": "/TimeSeries"
}

# Top Navigation Bar
navbar = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Img(
                        src="https://img.icons8.com/ios-filled/100/FFD700/globe-earth.png",
                        style={
                            'height': '40px',
                            'margin-right': '15px',
                            'borderRadius': '50%',
                            'background-color': '#001f3f',
                            'padding': '5px'
                        }
                    ),
                    html.H3("Incidentlytics", 
                           style={
                               'color': '#FFD700',
                               'margin': '0',
                               'font-weight': '700',
                               'font-family': 'Segoe UI, sans-serif'
                           })
                ], style={'display': 'flex', 'align-items': 'center'})
            ], width=4),
            dbc.Col([
                html.Div([
                    dbc.Nav([
                        dbc.NavLink(
                            k, 
                            href=f"{v}",
                            className="nav-link-custom",
                            active="exact",
                            style={
                                "color": "#FFD700",
                                "font-weight": "600",
                                "font-size": "16px",
                                "margin": "0 15px",
                                "padding": "8px 16px",
                                "border-radius": "20px",
                                "transition": "all 0.3s ease",
                                "text-decoration": "none"
                            }
                        ) for k, v in pages_dict.items()
                    ], 
                    className="d-flex justify-content-center align-items-center",
                    style={"height": "100%"}
                    )
                ])
            ], width=8, className="d-flex justify-content-center align-items-center")
        ], className="h-100")
    ], fluid=True, className="h-100")
], style=navbar_style)

# Sidebar with Filters (for Home page)
sidebar = html.Div([
    html.Div([
        html.H4("Filters", 
               style={
                   'color': '#001f3f',
                   'font-weight': '700',
                   'margin-bottom': '25px',
                   'text-align': 'center',
                   'font-family': 'Segoe UI, sans-serif'
               }),
        
        # Date Range Filter
        html.Div([
            html.Label("Date Range", 
                      style={
                          'color': '#001f3f',
                          'font-weight': '600',
                          'margin-bottom': '8px',
                          'display': 'block'
                      }),
            dcc.DatePickerRange(
                id='date-picker',
                display_format='YYYY-MM-DD',
                style={
                    "width": "100%",
                    "margin-bottom": "20px"
                }
            )
        ], className="mb-4"),
        
        # Country Filter
        html.Div([
            html.Label("Country", 
                      style={
                          'color': '#001f3f',
                          'font-weight': '600',
                          'margin-bottom': '8px',
                          'display': 'block'
                      }),
            dcc.Dropdown(
                id='country-dropdown',
                multi=True,
                placeholder="Select countries...",
                style={"margin-bottom": "20px"}
            )
        ], className="mb-4"),
        
        # Weather Condition Filter
        html.Div([
            html.Label("Weather Condition", 
                      style={
                          'color': '#001f3f',
                          'font-weight': '600',
                          'margin-bottom': '8px',
                          'display': 'block'
                      }),
            dcc.Dropdown(
                id='weather-dropdown',
                multi=True,
                placeholder="Select weather conditions...",
                style={"margin-bottom": "20px"}
            )
        ], className="mb-4"),
        
        # Clear Filters Button
        html.Div([
            dbc.Button(
                "Clear All Filters",
                id="clear-filters-btn",
                color="outline-primary",
                style={
                    "width": "100%",
                    "border-color": "#001f3f",
                    "color": "#001f3f",
                    "font-weight": "600"
                }
            )
        ], className="mb-4")
    ])
], style=sidebar_style)

# Empty Sidebar (for other pages)
empty_sidebar = html.Div([
    html.Div([
        html.H4("Filters", 
               style={
                   'color': '#001f3f',
                   'font-weight': '700',
                   'margin-bottom': '25px',
                   'text-align': 'center',
                   'font-family': 'Segoe UI, sans-serif'
               }),
        # You can add a logo or leave it empty for spacing
    ])
], style=sidebar_style)

# App Layout
app.layout = dmc.MantineProvider([
    dcc.Location(id="page-url"),
    navbar,
    html.Div(id="main-layout"),
    dcc.Markdown("""
        <style>
        .nav-link-custom:hover {
            background-color: #FFD700 !important;
            color: #001f3f !important;
            transform: translateY(-2px);
        }
        .nav-link-custom.active {
            background-color: #FFD700 !important;
            color: #001f3f !important;
        }
        .Select-control {
            border-color: #001f3f !important;
        }
        .Select-control:hover {
            border-color: #FFD700 !important;
        }
        .DateInput_input {
            border-color: #001f3f !important;
        }
        .DateInput_input:focus {
            border-color: #FFD700 !important;
        }
        </style>
    """, dangerously_allow_html=True)
])

# -------------------------------------------------- Page Layouts -------------------------------------------------- #

home_layout = create_insights_layout()
forecast_layout = create_forecast_layout()

@app.callback(
    Output("main-layout", "children"),
    Input("page-url", "pathname")
)
def display_page(pathname):
    if pathname == "/":
        # Home page: sidebar with filters
        return html.Div([
            sidebar,
            html.Div(home_layout, style=content_style)
        ])
    elif pathname == "/trends":
        # Trends page: empty sidebar for alignment
        return html.Div([
            empty_sidebar,
            html.Div(trends_layout, style=content_style)
        ])
    elif pathname == "/TimeSeries":
        # Forecast page: empty sidebar for alignment
        return html.Div([
            empty_sidebar,
            html.Div(forecast_layout, style=content_style)
        ])
    else:
        return html.Div([
            empty_sidebar,
            html.Div(
                html.H2("404 - Page Not Found", 
                        style={'text-align': 'center', 'color': '#001f3f', 'margin-top': '100px'}),
                style=content_style
            )
        ])

# Initialize filter options callback
@app.callback(
    [Output('date-picker', 'start_date'),
     Output('date-picker', 'end_date'),
     Output('date-picker', 'min_date_allowed'),
     Output('date-picker', 'max_date_allowed'),
     Output('country-dropdown', 'options'),
     Output('weather-dropdown', 'options')],
    Input('page-url', 'pathname')
)
def initialize_filters(pathname):
    # Import here to avoid circular import
    from pages.page1_home import df
    
    return (
        df['Date'].min(),
        df['Date'].max(), 
        df['Date'].min(),
        df['Date'].max(),
        [{'label': c, 'value': c} for c in sorted(df['Country'].unique())],
        [{'label': w, 'value': w} for w in sorted(df['Weather Condition'].unique())]
    )

# Clear filters callback
@app.callback(
    [Output('country-dropdown', 'value'),
     Output('weather-dropdown', 'value')],
    Input('clear-filters-btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_filters(n_clicks):
    if n_clicks:
        return None, None
    return None, None

if __name__ == "__main__":
    app.run(debug=True)