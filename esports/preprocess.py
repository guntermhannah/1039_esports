import pandas as pd
from esports.transform_data import average_player_data
from esports.get_wl_data import get_wl_data

def preprocess_pairs(user_steam_id, opps_steam_id):

    player_avg = average_player_data(user_steam_id)
    opponent_avg = average_player_data(opps_steam_id)
    player_wl = get_wl_data(user_steam_id)
    opponent_wl = get_wl_data(opps_steam_id)

    keys_to_transform = [
        'kills_per_min', 'deaths_per_min', 'assists_per_min', 'xp_per_min',
        'gold_per_min', 'hero_damage_per_min', 'tower_damage_per_min',
        'last_hits_per_min'
    ]

    for key in keys_to_transform:
        player_avg = player_avg.rename(index={key: f'player_{key}'})
        opponent_avg = opponent_avg.rename(index={key: f'opponent_{key}'})

    # Append win_ratio to player_avg and opponent_avg
    player_win_ratio = pd.Series(
        [player_wl["win"] / (player_wl["win"] + player_wl["lose"])],
        index=['player_win_ratio'])

    opponent_win_ratio = pd.Series(
        [opponent_wl["win"] / (opponent_wl["win"] + opponent_wl["lose"])],
        index=['opponent_win_ratio'])

    X_pred = player_avg.append(opponent_avg)
    X_pred = X_pred.append(player_win_ratio)
    X_pred = X_pred.append(opponent_win_ratio)

    X_pred = pd.DataFrame(X_pred)
    X_pred = X_pred.T

    return X_pred
