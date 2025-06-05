import numpy as np 
import pandas as pd 
from joblib import load        
import plotly.express as px  

# Dash 
import dash   
import dash_bootstrap_components as dbc 
from dash import Dash, html, dcc, Input, Output,State
  


#model = load('model.pkl')



app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO], suppress_callback_exceptions=True)
server = app.server


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


# Page Contenet Style
content_style = {
                    "margin-left": "16rem",
                    "margin-right": "0rem",
                    "padding": "20px",
                    "height": "100%",
                    "background-color": "#f3f3f3",  # Light Grey
                }



# Pages Navigator
pages_dict = {
                "Home" : "/",
                "Locations": "/Locations",
                "Experiences": "/experinces",
                "Forecast Accidents": "/TimeSeries"
            }



# Modal Alert
def get_alert(job_value, year_value):
    return dbc.Alert(
        [
                html.H2("Warning", style={"font":"bold 30px tahoma"}),
                html.P(
                    f"The Job {job_value} Did Not Exist In {year_value} !!😔😔",
                    style={"font":"bold 22px consolas"}
                ),
                html.Hr(),
                html.P(
                    "Choose Another Job",
                    style={"font":"bold 20px arial"},
                    className="mb-0",
                ),
            ], color="danger",
        style={"box-shadow": "none", "text-shdow":"none"}
    )



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


header=  html.H1(f"", id="header", style={"text-align":"center"})


# page content
content = html.Div(id="page-content", children = [], style = content_style)


# App Layout
app.layout = html.Div([
                        dcc.Location(id = "page-url"),
                        sidebar,
                        header,
                        content,
                      ], 
                    className="container-fluid")




# ----------------- Page Layouts ----------------- #

home_layout = html.Div([
    html.H2("Welcome to the Home Page"),
    html.P("This is the overview of the Incidentlytics Dashboard.")
])



locations_layout = html.Div([
    html.H2("Locations Page"),
    html.P("View and explore incidents by location.")
])



experiences_layout = html.Div([
    html.H2("Experiences Page"),
    html.P("This page contains user experiences or analysis.")
])



forecast_layout = html.Div([
    html.H2("Forecast Accidents Page"),
    html.P("This page will show accident forecasting using time series models.")
])






@app.callback(
    Output("page-content", "children"),
    Output("header", "children"),
    Input("page-url", "pathname")
)
def display_page(pathname):
    if pathname == "/":
        return home_layout, "Home"
    elif pathname == "/Locations":
        return locations_layout, "Locations"
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





# def create_high_salary_job_chart(year):

#     if year == "all":
#         df_filtered = df.copy()
#     else:
#         filt = df["Year"] == year
#         df_filtered = df[filt].copy()

#     df_filtered = df_filtered.groupby("Job_Title")["Salary_in_USD"].mean().sort_values(ascending=False).head(10)[::-1]

#     # Bar Chart of Wanted Job
#     fig_wanted_job = px.bar(df_filtered,
#                  y = df_filtered.index ,
#                  x = df_filtered ,
#                  orientation="h",
#                  color_discrete_sequence = ["#90CAF9"],
#                  title= "Jobs of the Highest Average Salary",
#                  labels={"Job_Title": "Job Title", "x": "AVG Salary (USD)"},
#                  template="plotly",
#                  text_auto = "0.3s"
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
#                    "size": 15,
#                     "color":"white"
#                    },
#         hovertemplate="Job Title: %{label}<br>AVG Salary: %{value}",
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
















# @app.callback(
#                 Output("prediction-placeholder", "children"),
#                 Input("deploy-button", "n_clicks"),
#                 State("deploy-job-menu", "value"),
#                 State("deploy-experience-menu", "value"),
#                 State("deploy-education-menu", "value"),
#                 State("deploy-company-size", "value"),
#                 State("deploy-industry-menu", "value"),
#                 State("deploy-location-menu", "value"),
#                 State("deploy-experience-years", "value"),
#             )

# def deploy_and_predict_salary(n, job_title, experience_level, experience_years, company_size, employment_type, location, remote_ratio):

#     if n is None:
#         return ""
    
#     print(f"Button Clicked: {n}")
#     print(f"Job Title: {job_title}")
#     print(f"Experience Level: {experience_level}")
#     print(f"Education Level: {experience_years}")
#     print(f"Company Size: {company_size}")
#     print(f"Industry: {employment_type}")
#     print(f"Location: {location}")
#     print(f"Experience Years: {remote_ratio}")
  
    
#     try:
#         # Construct input data as a DataFrame
#         input_data = {
#                         "work_year": [experience_years],
#                         "experience_level": [experience_level],
#                         "employment_type": [employment_type],
#                         "job_title": [job_title],
#                         "salary_currency": [location],
#                         "remote_ratio": [remote_ratio],
#                         "company_size": [company_size]
#                     }

#         input_df = pd.DataFrame(input_data)

#         # Load the preprocessor pipeline
#         preprocessor = load('preprocessor_pipeline.pkl')

#         # Transform input data using the preprocessor pipeline
#         transformed_data = preprocessor.transform(input_df)

#         print(f"Input Data: {transformed_data}")

#         # Reshape transformed data to 2D array
#         transformed_data = transformed_data.reshape(1, -1)

#         # Predict salary
#         y_pred = model.predict(transformed_data)[0]

#         print(f"Predicted Salary: ${y_pred:,.2f}")

#         return html.Div(html.Div(f"Predicted Salary: ${y_pred:,.2f}", style={"color": "red"}))

#     except Exception as e:
#         #print(f"Error predicting salary: {e}")
#         #return f"Error predicting salary: {e}"
#         pass


if __name__ == "__main__":
    app.run(debug=True)