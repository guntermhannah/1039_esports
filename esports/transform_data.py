from get_data import Dota2Api
import pandas as pd
import os

api = Dota2Api()

def transform_data():
    "This method retrieves data from matches and statistics and outputs it to a csv file"

    # retrieve matches data, append to matches csv
    matches_data = api.fetch_matches()
    matches_data.to_csv(os.path.join("data", "matches.csv"),
                        mode = "a", index = False, header=False)

    # loop through the matches data to get specific match infromation
    for i in range(len(matches_data)):

        # loop through specific match data and get player data
        match_id = matches_data['match_id'][i]
        player_stats_data = api.fetch_stats_data(match_id)

        if type(player_stats_data) == str:
            continue 

        # append player data to players
        player_stats_data.to_csv(os.path.join("data", "players.csv"),
                                                            mode = "a", index = False,
                                                            header=False)

transform_data()