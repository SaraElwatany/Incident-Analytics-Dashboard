import pandas as pd
import plotly.express as px
#from tools import plot_series



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