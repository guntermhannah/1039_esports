import pandas as pd
import os
import time
import requests

from matches_clean import clean_player_data, clean_matches_data
from transform_data import average_player_data


def wrapper(x):
    if type(average_player_data(x)) == str:
        empty_df ={'deaths_per_min':0, 
                'assists_per_min': 0, 
                'tower_damage_per_min': 0, 
                'xp_per_min': 0, 
                'gold_per_min': 0, 
                'kills_per_min': 0,
                'hero_damage_per_min': 0, 
                'last_hits_per_min': 0}
        return pd.DataFrame([empty_df.values()], columns = empty_df.keys())
    else:
        return average_player_data(x)


def get_wl_data(account_id):
    """retrieves win/loss data for an individual player, returns dict"""

    url = f"https://api.opendota.com/api/players/{account_id}/wl"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"win":0, "lose": 0}

    data = response.json()

    return data

def get_training_set():
    """returns dataframe of match_ids, with player and opponent account ids,
    winner, and player and opponent average stats over last 20 games"""

    # retrieve player data and match data
    player_data = clean_player_data()
    matches_data = clean_matches_data()

    # merge datasets
    df = player_data.merge(matches_data)

    # relevant features
    features = ['deaths_per_min', 
                'assists_per_min', 
                'tower_damage_per_min', 
                'xp_per_min', 
                'gold_per_min', 
                'kills_per_min',
                'hero_damage_per_min', 
                'last_hits_per_min', 
    ]

    # group player data by match_id, take the first account of winning and losing teams
    tmp = df[4000:].groupby(["match_id", "isRadiant"]).first()

    counter = 0
    # create df of pairs of winners and losers
    for match, new_df in tmp.groupby(level=[0]):
        game = {"match_id": 0,
                "player": 0,
                "player_deaths_per_min": 0,
                "player_assists_per_min": 0,
                "player_tower_damage": 0,
                "player_xp_per_min": 0,
                "player_gold_per_min":0,
                "player_net_worth":0,
                "player_kills_per_min":0,
                "player_hero_damage":0,
                "player_last_hits":0,
                "player_roshans_killed":0,
                "player_obs_placed":0,
                "opponent": 0,
                "opponent_deaths_per_min": 0,
                "opponent_assists_per_min": 0,
                "opponent_tower_damage": 0,
                "opponent_xp_per_min": 0,
                "opponent_gold_per_min":0,
                "opponent_net_worth":0,
                "opponent_kills_per_min":0,
                "opponent_hero_damage":0,
                "opponent_last_hits":0,
                "opponent_roshans_killed":0,
                "opponent_obs_placed":0,
                "winner": 0}
        game["match_id"] = match
        if len(new_df) !=2:
            continue
            
        # get player account_id
        player_account_id = str(int(new_df.loc[(match, False),"account_id"]))
        if len(player_account_id)<9:
            player_account_id = player_account_id + "0"*(9-len(player_account_id))
        game["player"] = player_account_id

        # get opponent account_id
        opponent_account_id = str(int(new_df.loc[(match, True),"account_id"]))
        if len(opponent_account_id)<9:
            opponent_account_id = opponent_account_id + "0"*(9-len(opponent_account_id))
        game["opponent"] = opponent_account_id

        # get winner info
        if new_df.loc[(match,False),"win"] == 1:
            game["winner"] = player_account_id
        else:
            game["winner"] = opponent_account_id


        game_df = pd.DataFrame([game.values()], columns = game.keys())
        
        # drop data without per min stats
        game_df = game_df.drop(columns = ["player_net_worth",
                                    "player_hero_damage", 
                                    "player_last_hits", 
                                    "opponent_net_worth",
                                    "opponent_hero_damage",
                                    "opponent_last_hits",
                                    ])

        # # get player and opponent average history
        try:
            for feature in features:
                game_df[f"player_{feature}"] = game_df["player"].apply(lambda x:wrapper(x)[feature])
                game_df[f"opponent_{feature}"] = game_df["opponent"].apply(lambda x:wrapper(x)[feature])
        except TypeError:
            continue


        # get player and opponent wl data
        player_wl_data = get_wl_data(player_account_id)
        if player_wl_data["win"] + player_wl_data["lose"] == 0:
            continue
        player_win_ratio = player_wl_data["win"]/(player_wl_data["lose"] + player_wl_data["win"])
        game_df["player_win_ratio"] = player_win_ratio

        opponent_wl_data = get_wl_data(opponent_account_id)
        if opponent_wl_data["win"] + opponent_wl_data["lose"] == 0:
            continue
        opponent_win_ratio = opponent_wl_data["win"]/(opponent_wl_data["lose"] +opponent_wl_data["win"])
        game_df["opponent_win_ratio"] = opponent_win_ratio


        game_df.to_csv(os.path.join("data", "player_pairs_avg_stats.csv"), mode = "a", index = False, header=False)

        counter += 1

        print(f"Added {counter} records")
        time.sleep(4)


get_training_set()
