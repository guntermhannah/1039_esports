import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder


def clean_matches_data():
    """Cleans the matches data from matches.csv file and returns a clean dataframe"""

    # Turn csv file into DataFrame
    df = pd.read_csv(os.path.join('data', 'matches.csv'))

    # Drop duplicates of match_id
    df.drop_duplicates(subset=['match_id'], inplace=True)

    # Drop avg_mmr NaN values
    df.dropna(subset=['avg_mmr'], inplace=True)

    # OrdinalEncoder the radiant_win column
    ordinal_encoder = OrdinalEncoder()
    df[['radiant_win']] = ordinal_encoder.fit_transform(df[['radiant_win']])

    return df


def clean_player_data():
    """Cleans the players data in the players.csv file, returns a clean dataframe.
    Drops any player data that does not have corresponding match in matches.csv"""

    df = pd.read_csv(os.path.join("data", "players.csv"))

    # drop duplicates
    df_clean = df.drop_duplicates()

    # missing data -- obs_placed and roshans_killed are rare achievements, can replace null values with 0
    df_clean["obs_placed"] = df_clean["obs_placed"].replace(np.nan, 0)
    df_clean["roshans_killed"] = df_clean["roshans_killed"].replace(np.nan, 0)

    # missing data -- missing account_id means it was a bot, not a player, drop those rows
    df_clean = df_clean.dropna()

    # drop player data that has been dropped from matches.csv
    matches = pd.read_csv(os.path.join("data", "matches.csv"))
    matches_list = matches["match_id"]

    for i in range(len(df_clean)):
        if df_clean[["match_id"]][i] not in matches_list:
            df_clean.drop([i], inplace=True)

    # one hot encode hero_id
    ohe = OneHotEncoder(sparse=False)
    ohe.fit(df_clean[["hero_id"]])
    df_clean[ohe.get_feature_names_out()] = ohe.transform(df_clean[["hero_id"
                                                                    ]])
    df_clean.drop(columns=["hero_id"], inplace=True)

    # drop rows where the player didnt win
    df_clean.drop(df_clean[df_clean['win'] == 1].index, inplace=True)

    return df_clean
