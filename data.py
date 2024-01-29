import os
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb

def fetch_dataset():
    dataframes = {}  # Dictionary to store the dataframes with file name as the key
    data_dir = "./data"

    for file in os.listdir(data_dir):
        df = pd.read_csv(os.path.join(data_dir, file))
        df['Date'] = pd.to_datetime(df['Date'], errors= 'coerce')
        df = df.dropna(subset=['Date'])
        
        # Extract year, month, day, hour, and minute components
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day
        df['Hour'] = df['Date'].dt.hour
        df['Minute'] = df['Date'].dt.minute
        
        # set date as index column
        df = df.set_index('Date')
        # drop rows and columns if all values are zero and empty
        df = df.dropna(how='all').dropna(axis=1, how='all').loc[:, (df != 0).any(axis=0)]
        
        # Leave columns with keyword of 'kW' and calculate sum of energy consumption of all floors 
        tmp1 = df.loc[:, df.columns.str.contains('kW')].groupby('Date').sum()
        # sum of energy consumption of all power outlets in all floors and zones
        tmp2 = tmp1.sum(axis=1).rename('total_demand').to_frame()
        df_powerMeter = pd.concat([tmp2, tmp1], axis=1)

        # mean of each T mins
        df_powerMeter = df_powerMeter.resample('10T').mean()

        # Extract the date components
        df_powerMeter['Year'] =  pd.DatetimeIndex(df_powerMeter.index).year
        df_powerMeter['Month'] = pd.DatetimeIndex(df_powerMeter.index).month
        df_powerMeter['Day'] = pd.DatetimeIndex(df_powerMeter.index).day
        df_powerMeter['Hour'] = pd.DatetimeIndex(df_powerMeter.index).hour
        df_powerMeter['Minute'] = pd.DatetimeIndex(df_powerMeter.index).minute

        df_powerMeter.index = pd.to_datetime(df_powerMeter.index, errors='coerce')
        df_powerMeter = df_powerMeter.dropna(axis=0, how='all')
        df_powerMeter.sort_values('Date')
        base_name = file[4:-4]
        print(base_name)
        # df_powerMeter = df_powerMeter[:100000] #for memory issues
        if base_name not in dataframes:
            dataframes[base_name] = df_powerMeter
        else:
            dataframes[base_name] = pd.concat([dataframes[base_name], df_powerMeter])
    
    return dataframes

def xgb_split(df):
    # Separate the target variable and features
    X = df.drop('total_demand', axis=1)
    # X = df_powerMeter
    y = df['total_demand']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)
    # Convert the data into DMatrix format for XGBoost
    train_data = xgb.DMatrix(X_train, label=y_train)
    test_data = xgb.DMatrix(X_test, label=y_test)
    
    return train_data, test_data

# def lstm_split(df, batch_size, n_clients):
#     # partition clients based on floors, each one represent a client and drop empty columns
#     client_data = [df[df['Floor'+str(i)] == 1.0].dropna(axis=1, how='all') for i in range (1, n_clients+1)]
#     client_loader = [torch.utils.data.DataLoader(x, batch_size=batch_size, shuffle=True) for x in client_data]
    
#     return client_loader, client_data