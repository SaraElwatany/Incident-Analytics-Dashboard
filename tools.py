import pandas as pd
import plotly.express as px




def monthly_casualties(accidents_df):

    # Convert to datetime and extract YearMonth
    accidents_df['Date'] = pd.to_datetime(accidents_df['Date'])
    accidents_df['YearMonth'] = accidents_df['Date'].dt.to_period('M')

    # Group by YearMonth and sum casualties
    monthly_counts = accidents_df.groupby('YearMonth')['Casualties'].sum().reset_index()

    # Convert YearMonth to timestamp
    monthly_counts['YearMonth'] = monthly_counts['YearMonth'].dt.to_timestamp()

    # Create and return Plotly figure
    fig = px.line(
                    monthly_counts,
                    x='YearMonth',
                    y='Casualties',
                    title='Monthly Casualties',
                    markers=True,
                    labels={'YearMonth': 'Month', 'Casualties': 'Number of Casualties'}
                )
    fig.update_traces(line=dict(dash='solid'))
    fig.update_layout(template='plotly_white')

    return fig








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







def get_casualties_features(accidents_df):

    #
    accidents_df_copy = accidents_df.copy()

    #
    accidents_df_copy['Date'] = pd.to_datetime(accidents_df_copy['Date'])
    accidents_df_copy['YearMonth'] = accidents_df_copy['Date'].dt.to_period('M')

    # Group by YearMonth and sum casualties
    monthly_counts = accidents_df_copy.groupby('YearMonth')['Casualties'].sum().reset_index()

    # Convert YearMonth to timestamp
    monthly_counts['YearMonth'] = monthly_counts['YearMonth'].dt.to_timestamp()

    # Create lag features (previous 3 months)
    for lag in range(1, 4):
        monthly_counts[f'lag_{lag}'] = monthly_counts['Casualties'].shift(lag)

    # Drop rows with NaN values created by shifting
    monthly_counts = monthly_counts.dropna().reset_index(drop=True)


    #
    last_known = monthly_counts[['Casualties']].tail(3)['Casualties'].values.tolist()
    
    #
    return monthly_counts, last_known
    








def get_accidents_features(accidents_df):
    
    #
    accidents_df_copy = accidents_df.copy()

    #
    accidents_df_copy['Date'] = pd.to_datetime(accidents_df_copy['Date'])
    accidents_df_copy['YearMonth'] = accidents_df_copy['Date'].dt.to_period('M')

    # Group by YearMonth and count accidents (Accident ID count or rows count)
    monthly_counts = accidents_df_copy.groupby('YearMonth').size().reset_index(name='AccidentsCount')

    # Convert YearMonth back to datetime for plotting
    monthly_counts['YearMonth'] = monthly_counts['YearMonth'].dt.to_timestamp()

    # Create lag features (previous 3 months)
    for lag in range(1, 4):
        monthly_counts[f'lag_{lag}'] = monthly_counts['AccidentsCount'].shift(lag)

    # Drop rows with NaN values created by shifting
    monthly_counts = monthly_counts.dropna().reset_index(drop=True)

    #
    last_known = monthly_counts[['AccidentsCount']].tail(3)['AccidentsCount'].values.tolist()


    #
    return monthly_counts, last_known