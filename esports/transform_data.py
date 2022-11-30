from esports.get_data import Dota2Api
import pandas as pd
import os
import time

api = Dota2Api()


def transform_data():
    "This method retrieves data from matches and statistics and outputs it to a csv file"

    # retrieve matches data, append to matches csv
    matches_data = api.fetch_matches()

    matches_data.to_csv(os.path.join("esports", "data", "matches.csv"),
                        mode="a",
                        index=False,
                        header=False)

    # loop through the matches data to get specific match infromation
    for i in range(len(matches_data)):

        # loop through specific match data and get player data
        match_id = matches_data['match_id'][i]
        player_stats_data = api.fetch_stats_data(match_id)

        if type(player_stats_data) == str:
            continue

        # append player data to players
        player_stats_data.to_csv(os.path.join("esports", "data",
                                              "players.csv"),
                                 mode="a",
                                 index=False,
                                 header=False)

        time.sleep(0.5)


def transform_player_data(account_id):
    """
    This method retrieves data from a players recent id, transforms it into
    and then outputs it to a csv file
    """
    # we make a call to the get_data method to retrieve the recent matches
    player_df = api.get_player_data(account_id)

    # append player data to players
    player_df.to_csv(os.path.join("esports", "data", "single_player_data.csv"),
                     mode="a",
                     index=False,
                     header=False)


def average_player_data(account_id):
    "This method collects recent games from an account id and returns the average stats"
    # retrieving the last games from the player
    player_df = api.get_player_data(account_id)

    if type(player_df) == str:
        return ""

    # we remove the columns we dont need
    player_df = player_df.drop(columns=[
        'game_mode', 'radiant_win', 'duration', 'match_id', 'lobby_type',
        'hero_id', 'average_rank'
    ])

    # we aggregate the results to retrieve the mean of each column
    player_df_mean = player_df.agg('mean')

    return player_df_mean


# to test the function average_player_data
#average_player_data(323271155)
