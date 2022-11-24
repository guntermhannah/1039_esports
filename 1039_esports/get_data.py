import requests
import os
import pandas as pd

api_key = os.environ["API_KEY"]

class Dota2Api():

    def __init__(self):
        #self.token = os.environ.get('API_KEY')
        self.url = 'https://api.opendota.com/api/'


    def fetch_matches(self):
        "This method gets random matches"
        # make API call
        url_ext = self.url + "publicMatches"
        params = {"api_key": api_key}

        response = requests.get(url_ext, params)
        #response = requests.get(url_ext)

        # check api call was successful
        if response.status_code != 200:
            return "Error"

        # parse results
        data = pd.DataFrame(response.json())
        stats = ["match_id", "radiant_win", "duration", "avg_mmr", "game_mode", "start_time"]
        stats_filtered = data[[stat for stat in stats]]

        return stats_filtered

    def fetch_stats_data(self, match_id):
        "This method gets stats data using a specified match id"
        # make API call
        url_ext = self.url + f"matches/{match_id}"
        params = {"api_key": api_key}

        response = requests.get(url_ext, params)
        #response = requests.get(url_ext)

        # check api call was successful
        if response.status_code != 200:
            return "Error"

        player_data = pd.DataFrame(response.json()["players"])

        #filter player data by relevent stats
        stats_keys = ['match_id', 'hero_id', 'account_id',
                    'net_worth', 'kills', 'deaths','hero_damage',
                    'gold_per_min', 'assists', 'xp_per_min',
                    'last_hits', 'tower_damage',
                    'obs_placed', 'roshans_killed', 'isRadiant','win'
        ]

        data = player_data[[stat for stat in stats_keys]]

        return data


    def get_player_data(self, account_id):
        "This method retrieves the 20 last games for a given player account id"
        # making the api request to get the json data of the last 20 games
        url_ext = self.url + f'/players/{account_id}/recentMatches'
        params = {"api_key": api_key}
        response = requests.get(url_ext, params).json()

        if response.status_code != 200:
            return ""

        # deciding the keys we are going to use
        player_keys = ['match_id', 'radiant_win', 'duration', 'game_mode', 'lobby_type',
                       'hero_id', 'kills', 'deaths', 'assists', 'average_rank',
                       'xp_per_min', 'gold_per_min', 'hero_damage', 'tower_damage',
                       'last_hits']

        # turning the response into a dataframe and keeping only the keys we need
        player_data = pd.DataFrame(response)

        player_df = player_data[[stat for stat in player_keys]]

        # we also want to transform some data to usable data like kills to kills per min
        keys_to_transform = ['kills', 'deaths', 'assists', 'hero_damage', 'tower_damage',
                            'last_hits']
        for key in keys_to_transform:

            # we go through every row and replace the specific key value with its value/duration
            player_df[key] = player_df.apply(lambda row: 60*row[key]/row['duration'], axis = 1)

            # we also change the name of the column to the key_per_min format
            player_df = player_df.rename(columns={key: f'{key}_per_min'})

        return player_df
