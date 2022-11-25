import pandas as pd
import os

from matches_clean import clean_player_data, clean_matches_data
from transform_data import average_player_data


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
    
    # clean and process wl data
    wl_data = pd.read_csv(os.path.join("data", "wl_data.csv"))
    wl_clean = wl_data[wl_data["wins"] != "wins"]
    wl_clean = wl_clean[wl_clean["total"] != "0"]
    wl_clean = wl_clean.drop_duplicates(subset="account_id", keep="last")
    wl_clean["account_id"] = wl_clean["account_id"].astype(int)
    wl_clean["win_ratio"] = wl_clean["wins"].astype(int)/wl_clean["total"].astype(int)


    # group player data by match_id, take the first account of winning and losing teams
    tmp = df[2200:].groupby(["match_id", "isRadiant"]).first()

    
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
        for feature in features:
            game_df[f"player_{feature}"] = game_df["player"].apply(lambda x:wrapper(x)[feature])
            game_df[f"opponent_{feature}"] = game_df["opponent"].apply(lambda x:wrapper(x)[feature])
        
        # merge wl data with player pair data
        merged = game_df.merge(wl_clean[["account_id", "win_ratio"]], left_on = "player", right_on = "account_id")
        merged["player_win_ratio"] = merged["win_ratio"]
        merged = merged.drop(columns= ["account_id", "win_ratio"])
        merged = merged.merge(wl_clean[["account_id", "win_ratio"]], left_on = "opponent", right_on = "account_id")
        merged["opponent_win_ratio"] = merged["win_ratio"]
        merged = merged.drop(columns= ["account_id", "win_ratio"])


        pd.DataFrame(game_df).to_csv(os.path.join("data", "player_pairs_avg_stats.csv"), mode = "a", index = False, header=False)


get_training_set()

def add_wl_data():
    """adds a wl column for player and opponent to training data"""

    # get player pair avg stats data
    df = pd.read_csv(os.path.join("data","player_pairs_avg_stats.csv"))
    df = df.dropna()


    # merge wl data with player pair data
    merged = df.merge(wl_clean[["account_id", "win_ratio"]], left_on = "player", right_on = "account_id")
    merged["player_win_ratio"] = merged["win_ratio"]
    merged = merged.drop(columns= ["account_id", "win_ratio"])
    merged = merged.merge(wl_clean[["account_id", "win_ratio"]], left_on = "opponent", right_on = "account_id")
    merged["opponent_win_ratio"] = merged["win_ratio"]
    merged = merged.drop(columns= ["account_id", "win_ratio"])

    merged.to_csv(os.path.join("data","player_pairs_avg_stats.csv"), mode = "w", index = False, header = True)
