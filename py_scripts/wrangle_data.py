import pandas as pd
import numpy as np

def prep_data():
    """
    Prepares San Francisco crime data.

    parameters:
    -----------
    None
    
    returns:
    --------
    pandas.DataFrame
        wrangled dataset
    """
    # read data
    df = pd.read_csv("data/SF-crime-data_2016.csv")

    # convert to datetime and extract hour
    df['datetime'] = pd.to_datetime(df[["Date","Time"]].apply(lambda x: x[0].split()[0] +" "+x[1], axis=1), format="%m/%d/%Y %H:%M")
    df['hour'] = df['datetime'].dt.hour     
    df.dropna(inplace=True)
    
    # filter out top 4 crimes
    top_4_crimes = df['Category'].value_counts()[:6].index.to_list()
    top_4_crimes
    top_4_crimes.remove("NON-CRIMINAL")
    top_4_crimes.remove("OTHER OFFENSES")

    return df[df["Category"].isin(top_4_crimes)]