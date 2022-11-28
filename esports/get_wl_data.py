import requests
import pandas as pd
import os
import time

from esports.matches_clean import clean_player_data


api_key = os.environ.get('API_KEY')


def get_wl_data(account_id):
    """retrieves win/loss data for an individual player, returns dict"""

    url = f"https://api.opendota.com/api/players/{account_id}/wl"
    params = {"api_key": api_key}

    response = requests.get(url, params)

    if response.status_code != 200:
        return {"win":0, "lose": 0}

    data = response.json()

    return data

def build_wl_dataset():
    """builds csv file of individual player win/loss data"""

    player_pairs = pd.read_csv(os.path.join("data","player_pairs_avg_stats.csv"))

    for i in range(len(player_pairs)):
        #get player wl data
        account_id = str(int(player_pairs.iloc[i,1]))
        if len(account_id)<9:
            account_id = account_id + "0"*(9-len(account_id))
        data = get_wl_data(account_id)
        win_loss = {"account_id":account_id,"wins":data["win"],"losses":data["lose"], "total" :data["win"]+data["lose"]}

        df = pd.DataFrame([win_loss.values()], columns = win_loss.keys())
        
        df.to_csv(os.path.join("data", "wl_data.csv"), mode = "a", index = False, header=False)

        #get opponent wl data
        account_id = str(int(player_pairs.iloc[i,10]))
        if len(account_id)<9:
            account_id = account_id + "0"*(9-len(account_id))
        data = get_wl_data(account_id)
        win_loss = {"account_id":account_id,"wins":data["win"],"losses":data["lose"], "total" :data["win"]+data["lose"]}

        df = pd.DataFrame([win_loss.values()], columns = win_loss.keys())
        
        df.to_csv(os.path.join("data", "wl_data.csv"), mode = "a", index = False, header=False)

        time.sleep(1)

build_wl_dataset()


def get_match_pairs():
    """returns dataframe of match_ids, with player account_id, opponent account_id, and who won"""
    # retrieve player data
    player_data = clean_player_data()

    # group player data by match_id, take the first account of winning and losing teams
    tmp = player_data.groupby(["match_id", "isRadiant"]).first()

    #create df of pairs of winners and losers
    games = []
    for match, new_df in tmp.groupby(level=[0]):
        game = {"match_id": 0,
                "player": 0,
                "opponent": 0,
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
        games.append(game)

    pd.DataFrame(games).to_csv(os.path.join("esports", "data", "player_pairs.csv"), mode = "a", index = False, header=True)

<<<<<<< HEAD:1039_esports/get_wl_data.py
=======

get_match_pairs()
>>>>>>> master:esports/get_wl_data.py
