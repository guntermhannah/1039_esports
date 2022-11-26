import pandas as pd
import os
import time

from matches_clean import clean_player_data, clean_matches_data
from transform_data import average_player_data
from get_wl_data import get_wl_data


def wrapper(x):
    if type(average_player_data(x)) == str:
        return {'deaths_per_min':None, 
                'assists_per_min': None, 
                'tower_damage_per_min': None, 
                'xp_per_min': None, 
                'gold_per_min': None, 
                'kills_per_min': None,
                'hero_damage_per_min': None, 
                'last_hits_per_min': None
        }
    else:
        return average_player_data(x)


def get_training_set():
    """returns dataframe of match_ids, with player and opponent account ids,
    winner, and player and opponent average stats over last 20 games"""
    
    print("Checkpoint 0")

    # retrieve player data and match data
    player_data = clean_player_data()
    matches_data = clean_matches_data()

    # merge datasets
    df = player_data.merge(matches_data)

    print("Checkpoint 1")

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
    print("Checkpoint 2")

    # group player data by match_id, take the first account of winning and losing teams
    tmp = df[3000:].groupby(["match_id", "isRadiant"]).first()

    print("Checkpoint 3")
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

        print("Checkpoint 4")
            
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

        print("Checkpoint 5")
                
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
        for feature in features:
            game_df[f"player_{feature}"] = game_df["player"].apply(lambda x:wrapper(x)[feature])
            game_df[f"opponent_{feature}"] = game_df["opponent"].apply(lambda x:wrapper(x)[feature])
        
        print("Checkpoint 6")

        player_wl_data = get_wl_data(player_account_id)

        print(player_wl_data)

        # # # merge wl data with player pair data
        # player_wl_stats = wl_clean[wl_clean["account_id"] == player_account_id]
        # opponent_wl_stats = wl_clean[wl_clean["account_id"] == opponent_account_id]



        # merged = game_df.merge(wl_clean[["account_id", "win_ratio"]], left_on = "player", right_on = "account_id")
        # merged["player_win_ratio"] = merged["win_ratio"]
        # merged = merged.drop(columns= ["account_id", "win_ratio"])
        # merged = merged.merge(wl_clean[["account_id", "win_ratio"]], left_on = "opponent", right_on = "account_id")
        # merged["opponent_win_ratio"] = merged["win_ratio"]
        # merged = merged.drop(columns= ["account_id", "win_ratio"])

        # print("Checkpoint 7")
        # print(merged)

        # merged_df = pd.DataFrame(merged)
        game_df.to_csv(os.path.join("data", "player_pairs_avg_stats.csv"), mode = "a", index = False, header=False)

        print("Checkpoint 8")
        print(game_df)


        time.sleep(2)


get_training_set()
