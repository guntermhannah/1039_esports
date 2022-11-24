import pandas as pd
import os

def get_win_ratio():

    # Turn csv file into DataFrame
    df = pd.read_csv(os.path.join('data', 'wl_data.csv'))

    # Drop duplicates of account_id
    df.drop_duplicates(subset=['account_id'], inplace=True)

    # Create ratio column
    df['wl_ratio'] = df['win'] / df['total']

    # Sum ratio column
    percentage = df['wl_ratio'].sum() / len(df['wl_ratio'])

    return percentage
