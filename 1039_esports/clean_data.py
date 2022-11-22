import numpy as np
import pandas as pd
import os

def clean_player_data():
    """Cleans the players data in the players.csv file, returns a clean dataframe. 
    Drops any player data that does not have corresponding match in matches.csv"""

    df = pd.read_csv(os.path.join("data","players.csv"))
    
    # drop duplicates
    df_clean = df.drop_duplicates()

    # missing data -- obs_placed and roshans_killed are rare achievements, can replace null values with 0
    df_clean["obs_placed"] = df_clean["obs_placed"].replace(np.nan, 0)
    df_clean["roshans_killed"] = df_clean["roshans_killed"].replace(np.nan, 0)

    # missing data -- missing account_id means it was a bot, not a player, drop those rows
    df_clean = df_clean.dropna()

    # drop player data that has been dropped from matches.csv
    matches = pd.read_csv(os.path.join("data","matches.csv"))
    matches_list = matches["match_id"]

    for i in range(len(df)):
        if df[["match_id"]][i] not in matches_list:
            df_clean.drop([i], inplace = True)



    return df_clean