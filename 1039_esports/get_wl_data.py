import requests
import pandas as pd
import os

from matches_clean import clean_player_data

def get_wl_data(account_id):
    """retrieves win/loss data for an individual player, returns dict"""

    url = f"https://api.opendota.com/api/players/{account_id}/wl"
    
    response = requests.get(url)

    data = response.json()

    return data

def build_wl_dataset():
    """builds csv file of individual player win/loss data"""

    player_data = clean_player_data()
    all_players = []

    for i in range(len(player_data)):
        account_id = str(int(player_data.iloc[i,2]))
        if len(account_id)<9:
            account_id = account_id + "0"*(9-len(account_id))
        data = get_wl_data(account_id)
        win_loss = [account_id, data["win"], data["lose"], data["win"]+data["lose"]]
        all_players.append(win_loss)

    df = pd.DataFrame(all_players, columns=["account_id", "wins", "losses", "total"])

    df.to_csv(os.path.join("data", "wl_data.csv"), mode = "a", index = False, header=True)

build_wl_dataset()