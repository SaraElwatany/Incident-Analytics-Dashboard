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






# Sidebar Style
sidebar_style = {
                    "position": "fixed",
                    "width": "20rem",
                    "height": "100vh",
                    "top": "0",
                    "bottom": "0",
                    "left": "0",
                    "padding": "20px",
                    "background-color": "#001f3f",                  # Navy Blue
                    "font-family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",  
                    "font-size": "25px",  
                    "font-weight": "500",  
                    "color": "#FFD700",                 # Yellow text
                }



# Page Content Style
content_style = {
                    "margin-left": "16rem",
                    "margin-right": "0rem",
                    "padding": "30px",
                    "height": "100%",
                    "background-color": "#f3f3f3",          # Light Grey
                }




# Pages Navigator
pages_dict = {
                "Home" : "/",
                "Trends": "/trends",
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
                                    "color": "#f3f3f3" , # Yellow text
                                    "font-weight": "600",
                                    "border": "1px solid #f3f3f3",
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



# page content
content = html.Div(id="page-content", children = [], style = content_style)


# App Layout
app.layout = dmc.MantineProvider(
                                    children=[
                                        html.Div([
                                                    dcc.Location(id="page-url"),
                                                    sidebar,
                                                    content,
                                                ], className="container-fluid")
                                    ]
                                )




# -------------------------------------------------- Home Page Layout -------------------------------------------------- #

home_layout = create_insights_layout()






# -------------------------------------------------- Forecasting Page Layout -------------------------------------------------- #


forecast_layout = create_forecast_layout()








@app.callback(
    Output("page-content", "children"),
    Input("page-url", "pathname")
)
def display_page(pathname):

    if pathname == "/":
        return home_layout
    elif pathname == "/trends":
        return trends_layout 
    elif pathname == "/TimeSeries":
        return forecast_layout
    else:
        return html.Div([html.H2("404 - Page Not Found")])







if __name__ == "__main__":
    app.run()