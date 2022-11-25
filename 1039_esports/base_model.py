import pandas as pd
import os
import numpy as np
from sklearn.metrics import accuracy_score

def get_player_ratio(account_id:int)->float:

    # Get the data for player_pairs and wl_data
    df_wl = pd.read_csv(os.path.join('data', 'wl_data.csv'))

    ###
    #row = df_wl[df_wl['account_id'] == account_id]
    #print(int(row['total']))

    df_wl = df_wl[df_wl['total'] != 0]
    df_wl.drop_duplicates(subset=['account_id'], inplace=True)

    # Check if account_id is in the wl_data.csv
    if account_id in df_wl['account_id'].values:
        # Find that row
        row = df_wl[df_wl['account_id'] == account_id]
        # Calculate ratio
        ratio = int(row['wins']) / int(row['total'])
        return ratio

    # Return -1.0 value if not found in csv
    return -1.0


def column_e():

    df_pairs = pd.read_csv(os.path.join('data', 'player_pairs.csv'))

    # y_pred = if player wins
    y_pred = []
    y_true = []

    #player_list = []
    #opponent_list = []

    for row in range(0, len(df_pairs)):

        # Get the account_id of player and opponent
        player_id = int(df_pairs['player'][row])
        opponent_id = int(df_pairs['opponent'][row])
        winner_id = int(df_pairs['winner'][row])

        # Get the ratios of each player
        player_ratio = get_player_ratio(player_id)
        opponent_ratio = get_player_ratio(opponent_id)

        #player_list.append(player_ratio)
        #opponent_list.append(opponent_ratio)
        #test = pd.DataFrame({'players': player_list, 'opponents':opponent_list})

        # Find prediction only if both players have ratio from wl_data
        if (player_ratio > 0) and (opponent_ratio > 0):

            # Determine if player won
            if (player_ratio > opponent_ratio):
                y_pred.append(1)
            else:
                y_pred.append(0)

            if (player_id == winner_id):
                y_true.append(1)
            else:
                y_true.append(0)

        else:
            pass

    # Determine accuary
    accuracy = accuracy_score(y_true, y_pred)

    return accuracy

column_e()
