from get_data import Dota2Api
import pandas as pd
import os
import time

api = Dota2Api()

def transform_data():
    "This method retrieves data from matches and statistics and outputs it to a csv file"

    # retrieve matches data, append to matches csv
    matches_data = api.fetch_matches()

    matches_data.to_csv(os.path.join("1039_esports", "data", "matches.csv"),
                        mode = "a", index = False, header=False)
    
    
        
    # loop through the matches data to get specific match infromation
    for i in range(len(matches_data)):

        # loop through specific match data and get player data
        match_id = matches_data['match_id'][i]
        player_stats_data = api.fetch_stats_data(match_id)

        if type(player_stats_data) == str:
            continue

        # append player data to players
        player_stats_data.to_csv(os.path.join("1039_esports", "data", "players.csv"),
                                                            mode = "a", index = False,
                                                            header=False)

        time.sleep(0.5)


def transform_player_data(account_id):
    """
    This method retrieves data from a players recent id, transforms it into
    and then outputs it to a csv file
    """

    # we make a call to the get_data method to retrieve the recent matches
    player_df = api.get_player_data(account_id)

    # we also want to transform some data to usable data like kills to kills per min
    keys_to_transform = ['kills', 'deaths', 'assists', 'hero_damage', 'tower_damage',
                         'last_hits']
    for key in keys_to_transform:

        # we go through every row and replace the specific key value with its value/duration
        player_df[key] = player_df.apply(lambda row: 60*row[key]/row['duration'], axis = 1)

        # we also change the name of the column to the key_per_min format
        player_df = player_df.rename(columns={key: f'{key}_per_min'})

    # append player data to players
    player_df.to_csv(os.path.join("1039_esports", "data", "single_player_data.csv"),
                                                        mode = "a", index = False,
                                                        header=False)
