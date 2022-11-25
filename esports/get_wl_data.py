import requests
import pandas as pd
import os

from esports.matches_clean import clean_player_data
from esports.get_data import Dota2Api

api = Dota2Api()


def build_wl_dataset():
    """builds csv file of individual player win/loss data"""

    player_data = clean_player_data()
    all_players = []

    for i in range(500):
        account_id = str(int(player_data.iloc[i,2]))
        if len(account_id)<9:
            account_id = account_id + "0"*(9-len(account_id))
        data = api.get_wl_data(account_id)
        win_loss = [account_id, data["win"], data["lose"], data["win"]+data["lose"]]
        all_players.append(win_loss)

    df = pd.DataFrame(all_players, columns=["account_id", "wins", "losses", "total"])

    df.to_csv(os.path.join("data", "wl_data.csv"), mode = "a", index = False, header=True)


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


get_match_pairs()
