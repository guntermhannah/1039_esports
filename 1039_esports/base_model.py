import pandas as pd
import os
import numpy as np

def get_player_ratio(account_id:int)->float:

    # Get the data for player_pairs and wl_data
    df_wl = pd.read_csv(os.path.join('data', 'wl_data.csv'))

    # Remove rows where total == 0
    df_wl = df_wl[df_wl['total'] != 0]

    # Check if account_id is in the wl_data.csv
    if account_id in df_wl['account_id'].values:
        # Find that row
        row = df_wl[df_wl['account_id'] == account_id]
        # Calculate ratio
        ratio = int(row['wins']) / int(row['total'])
        return float(ratio)

    # Return -1.0 value if not found in csv
    return -1.0


def column_e():

    df_pairs = pd.read_csv(os.path.join('data', 'player_pairs.csv'))

    # y_pred = if player wins
    y_pred = []
    y_true = []

    for row in range(0, len(df_pairs)):

        # Get the account_id of player and opponent
        player_id = int(df_pairs['player'][row])
        opponent_id = int(df_pairs['opponent'][row])
        winner_id = int(df_pairs['winner'][row])

        # Get the ratios of each player
        player_ratio = get_player_ratio(player_id)
        opponent_ratio = get_player_ratio(opponent_id)

        # Find prediction only if both players have ratio from wl_data
        if (player_ratio > 0) and (opponent_ratio > 0):

            # Determine if player won
            if (player_ratio > opponent_ratio):
                y_pred.append(1)
            else:
                y_pred.append(0)

            y_pred = np.array([y_pred])

            if (player_id == winner_id):
                y_true.append(1)
            else:
                y_true.append(0)

            y_true = np.array([y_true])

        else:
            pass

    pass

column_e()
