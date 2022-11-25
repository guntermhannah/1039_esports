import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split


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

    # drop rows where the player didnt win
    # df_clean.drop(df_clean[df_clean['win'] == 0].index, inplace=True)

    return df_clean


def clean_player_pairs_data():
    """Cleans the player pairs avg stats data in the player_pairs_avg_stats.csv
    file, returns a clean dataframe."""

    # load csv and convert to DataFrame
    df = pd.read_csv(os.path.join("data", "player_pairs_avg_stats.csv"))

    # drop duplicates
    df_clean = df.drop_duplicates()

    # drop na
    df_clean = df.dropna()

    # add new column to indicate player's win
    df_clean['player_win'] = np.where(df_clean["player"] == df_clean["winner"], 1, 0)

    return df_clean


def train_test_split_data():
    """Drops id columns, roshans killed, and obs placed from player pairs avg
    stats df. Splits data into train/test split."""

    df = clean_player_pairs_data()
    X = df.drop(columns=[
        'match_id', 'player', 'opponent', 'winner', 'player_roshans_killed',
        'player_obs_placed', 'opponent_roshans_killed', 'opponent_obs_placed', 'player_win'
    ])
    y = df['player_win']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    return X_train, X_test, y_train, y_test

X, n, y, m = train_test_split_data()
print(X.columns)