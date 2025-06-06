import pandas as pd
import matplotlib.pyplot as plt



# # Model Alert
# def get_alert(job_value, year_value):
#     return dbc.Alert(
#         [
#                 html.H2("Warning", style={"font":"bold 30px tahoma"}),
#                 html.P(
#                     f"The Job {job_value} Did Not Exist In {year_value} !!😔😔",
#                     style={"font":"bold 22px consolas"}
#                 ),
#                 html.Hr(),
#                 html.P(
#                     "Choose Another Job",
#                     style={"font":"bold 20px arial"},
#                     className="mb-0",
#                 ),
#             ], color="danger",
#         style={"box-shadow": "none", "text-shdow":"none"}
#     )


def plot_series(x_data, y_data, title, x_label, y_label, labels=[], linestyles=[]):

    """
    Plots multiple time series on the same figure.

    Args:
      x_data : list of array-like
          List containing x-axis data for each series (e.g., list of datetime arrays).
      
      y_data : list of array-like
          List containing y-axis data for each series (e.g., casualties, counts, etc.).
      
      title : str
          Title of the plot.
      
      x_label : str
          Label for the x-axis.
      
      y_label : str
          Label for the y-axis.
      
      labels : list of str, optional
          List of labels for each series (for the legend). Default is an empty list.
      
      linestyles : list of str, optional
          List of line styles for each series (e.g., '-', '--', '-.', ':'). Default is an empty list.

    Returns:
      None
          Displays the plot.
    """

    # Single figure for all lines
    plt.figure(figsize=(12,6))

    # Plot Individual lines
    for x, y, label, line_style in zip(x_data, y_data, labels, linestyles):

        plt.plot(x, y, marker='o', label=label, linestyle=line_style)

    # Set Title & Axes Labels
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Display the Plot
    plt.grid(True)
    plt.show()










def forecast_interval(model, monthly_counts, n_forecast, last_known):

    """
    Forecasts future monthly accident counts using a trained model and lagged inputs.

    This function uses the last 3 known monthly values to iteratively predict the 
    next `n_forecast` months.

    Args:
      model : sklearn.models
          The trained model on our historical data.

      monthly_counts : pandas.DataFrame
          The original DataFrame containing historical monthly accident counts. 
          Must include a 'YearMonth' column with datetime-like entries.
      
      n_forecast : int
          The number of future months to forecast.
      
      last_known : list of float
          A list of the most recent known or predicted values (e.g., accident counts), 
          from which the model will generate lag-based forecasts. 
          Must contain at least 3 values.

    Returns:
      future_dates : pandas.DatetimeIndex
          A datetime index corresponding to the forecasted months.
      
      future_predictions : list of float
          List of predicted values for each forecasted month.
    
    Notes:
    ------
    - This function assumes a global `model` (e.g., an XGBoost regressor) is already trained.
    - The forecast is recursive: predictions are fed back as inputs for future steps.
    - `last_known` is modified in-place by appending the predictions.
    """

    future_predictions = []

    for i in range(n_forecast):

        # Create input features from last 3 months
        x_input = pd.DataFrame([last_known[-1], last_known[-2], last_known[-3]]).T
        x_input.columns = ['lag_1', 'lag_2', 'lag_3']
        x_input = x_input[['lag_1', 'lag_2', 'lag_3']]  
        
        # Predict next month
        y_pred = model.predict(x_input)[0]
        future_predictions.append(y_pred)
        
        # Append prediction to last_known to roll forward
        last_known.append(y_pred)

    # Build future dates index for plotting
    last_date = monthly_counts['YearMonth'].iloc[-1]
    future_dates = pd.date_range(start=last_date + pd.offsets.MonthBegin(1), periods=n_forecast, freq='MS')

    return future_dates, future_predictions