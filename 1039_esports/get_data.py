import requests
import os
import pandas as pd

api_key = os.environ["API_KEY"]


def fetch_matches(is_first = False):
    #make API call
    url = "https://api.opendota.com/api/publicMatches"
    params = {"api_key": api_key}

    response = requests.get(url, params)

    #check api call was successful
    if response.status_code != 200:
        return "Error: status code ", response.status_code

    #parse results
    data = pd.DataFrame(response.json())

    #append newly fetched data to matches.csv
    path = os.path.join("..", "raw_data", "matches.csv")
    data.to_csv(path,
                header = is_first,
                index = False)
