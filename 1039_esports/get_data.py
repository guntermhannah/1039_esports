import requests
import os
import pandas as pd

api_key = os.environ["API_KEY"]

class Dota2Api():

    def __init__(self):
        self.token = os.environ.get('API_KEY')
        self.url = 'https://api.opendota.com/api/'


    def fetch_matches(self):
        "This method gets random matches"
        # make API call
        url = "https://api.opendota.com/api/publicMatches"
        params = {"api_key": api_key}

        response = requests.get(url, params)
        # response = requests.get(url)

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
        url = f"https://api.opendota.com/api/matches/{match_id}"
        params = {"api_key": api_key}

        response = requests.get(url, params)
        # response = requests.get(url)

        # check api call was successful
        if response.status_code != 200:
            return "Error"

        player_data = pd.DataFrame(response.json()["players"])

        #filter player data by relevent stats
        stats_keys = ['match_id', 'hero_id', 'account_id',
                    'net_worth', 'kills', 'deaths','hero_damage',
                    'gold_per_min', 'assists', 'xp_per_min', 
                    'last_hits', 'tower_damage',
                    'obs_placed', 'roshans_killed', "isRadiant", "win"
        ]

        data = player_data[[stat for stat in stats_keys]]

        return data

