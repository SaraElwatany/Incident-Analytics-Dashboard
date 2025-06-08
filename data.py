import pandas as pd 


def determine_severity(row):
    if row['Casualties'] >= 6 or row['Vehicles Involved'] >= 4:
        return 'Severe'
    elif 2 <= row['Casualties'] <= 5 and row['Vehicles Involved'] <= 3:
        return 'Moderate'
    else:
        return 'Minor'



def get_time_segment(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'

def data_preprocess(path):
    accidents_df = pd.read_csv('dataset/global_traffic_accidents.csv')
    accidents_df['City'] = accidents_df['Location'].map(lambda x:x.split(',')[0])
    accidents_df['Country'] = accidents_df['Location'].map(lambda x:x.split(',')[1])
    accidents_df['Date'] = pd.to_datetime(accidents_df['Date'])
    accidents_df['Year'] = accidents_df['Date'].dt.year 
    accidents_df['Month_Num'] = accidents_df['Date'].dt.month       
    accidents_df['Hour'] = pd.to_datetime(accidents_df['Time'], format='%H:%M').dt.hour
    accidents_df['Time Segment'] = accidents_df['Hour'].apply(get_time_segment)
    accidents_df['Severity'] = accidents_df.apply(determine_severity, axis=1)
    accidents_df['YearMonth'] = accidents_df['Date'].dt.to_period('M')
    return accidents_df