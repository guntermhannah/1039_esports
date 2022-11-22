import os
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder


def clean_matches_data():
    """Cleans the matches data from matches.csv file and returns a clean dataframe"""

    # Turn csv file into DataFrame
    df = pd.read_csv(os.path.join('data', 'matches.csv'))

    # Drop duplicates of match_id
    df.drop_duplicates(subset='match_id', inplace=True)

    # Drop avg_mmr NaN values
    df.dropna(subset='avg_mmr', inplace=True)

    # OrdinalEncoder the radiant_win column
    ordinal_encoder = OrdinalEncoder()
    df[['radiant_win']] = ordinal_encoder.fit_transform(df[['radiant_win']])

    return df
