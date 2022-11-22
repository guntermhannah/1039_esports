import numpy as np
import pandas as pd
import os

def clean_player_data():
    """This function cleans the players data in the players.csv file, returns a clean dataframe"""
    df = pd.read_csv(os.path.join("data","players.csv"))
    
    # drop duplicates
    df_clean = df.drop_duplicates()

    # missing data -- obs_placed and roshans_killed are rare achievements, can replace null values with 0
    df_clean["obs_placed"] = df_clean["obs_placed"].replace(np.nan, 0)
    df_clean["roshans_killed"] = df_clean["roshans_killed"].replace(np.nan, 0)

    # missing data -- missing account_id means it was a bot, not a player, drop those rows
    df_clean = df_clean.dropna()

    print(df_clean.isnull().sum()/len(df))

clean_player_data()