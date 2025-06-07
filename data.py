import pandas as pd 


def determine_severity(row):
    if row['Casualties'] >= 6 or row['Vehicles Involved'] >= 4:
        return 'Severe'
    elif 2 <= row['Casualties'] <= 5 and row['Vehicles Involved'] <= 3:
        return 'Moderate'
    else:
        return 'Minor'

def data_preprocess(path):
    accidents_df = pd.read_csv('dataset/global_traffic_accidents.csv')
    accidents_df['City'] = accidents_df['Location'].map(lambda x:x.split(',')[0])
    accidents_df['Country'] = accidents_df['Location'].map(lambda x:x.split(',')[1])
    accidents_df['Date'] = pd.to_datetime(accidents_df['Date'])
    accidents_df['Time']=pd.to_datetime(accidents_df['Time'],format='%H:%M').dt.time
    accidents_df['Severity'] = accidents_df.apply(determine_severity, axis=1)
    return accidents_df