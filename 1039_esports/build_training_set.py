import pandas as pd
import os

from matches_clean import clean_player_data, clean_matches_data


def get_training_set():
    """returns dataframe of match_ids, with player account_id, opponent account_id, and who won"""
    # retrieve player data and match data
    player_data = clean_player_data()
    matches_data = clean_matches_data()

    # merge datasets
    df = player_data.merge(matches_data)

    # feature manipulation -- creating per min stats
    df["deaths_per_min"] = df["deaths"]/df["duration"]
    df["kills_per_min"] = df["kills"]/df["duration"]
    df["assists_per_min"] = df["assists"]/df["duration"]

    # relevant features
    features = ['deaths_per_min', 
                'assists_per_min', 
                'tower_damage', 
                'xp_per_min', 
                'gold_per_min', 
                'net_worth',
                'kills_per_min',
                'hero_damage', 
                'last_hits', 
                'hero_id',
                'roshans_killed', 
                'obs_placed'
    ]


    # group player data by match_id, take the first account of winning and losing teams
    tmp = df.groupby(["match_id", "isRadiant"]).first()
    
    #create df of pairs of winners and losers
    games = []
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
                "player_hero_id":0,
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
                "opponent_hero_id":0,
                "opponent_roshans_killed":0,
                "opponent_obs_placed":0,
                "winner": 0}
        game["match_id"] = match
        if len(new_df) !=2:
            continue
            
        # get player account_id
        player_account_id = str(int(new_df.iloc[0,1]))
        if len(player_account_id)<9:
            player_account_id = player_account_id + "0"*(9-len(player_account_id))
        game["player"] = player_account_id

        # get opponent account_id
        opponent_account_id = str(int(new_df.iloc[1,1]))
        if len(opponent_account_id)<9:
            opponent_account_id = opponent_account_id + "0"*(9-len(opponent_account_id))
        game["opponent"] = opponent_account_id

        # get winner info
        if new_df.iloc[0,-1] == 1:
            game["winner"] = player_account_id
        else:
            game["winner"] = opponent_account_id
            
        # get player and opponent stats
        for feature in features:
            game[f"player_{feature}"] = new_df.loc[(match,False), feature]
            game[f"opponent_{feature}"] = new_df.loc[(match,True), feature]
                
        games.append(game)

    pd.DataFrame(games).to_csv(os.path.join("data", "player_pairs_stats.csv"), mode = "a", index = False, header=True)
        

get_training_set()