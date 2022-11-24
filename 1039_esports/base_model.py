import pandas as pd
import os
from matches_clean import clean_player_data

def get_win_ratio():

    # Turn csv file into DataFrame
    df = pd.read_csv(os.path.join('data', 'wl_data.csv'))

    # Drop duplicates of account_id
    df.drop_duplicates(subset=['account_id'], inplace=True)

    # Create ratio column
    df['wl_ratio'] = df['win'] / df['total']

    # Sum ratio column
    win_rate = df['wl_ratio'].sum() / len(df['wl_ratio'])

    return win_rate



def win_ratio():

    # Turn csv file into DataFrame
    df = jasmine_get()

    # Grab account_id
    player1 = df['player_1'][0]
    player2 = df['player_2'][0]

    # Determine how many wins that account_id has against the other account_id
    player1_wins = df.won_id.value_counts().player1
    player2_wins = df.won_id.value_counts().player2

    # Determine the win percentage of player1
    ratio = player1_wins / player2_wins

    return ratio
