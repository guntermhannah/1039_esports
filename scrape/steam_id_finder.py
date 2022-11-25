from bs4 import BeautifulSoup
import requests

#SEARCH_URL = 'https://www.steamidfinder.com/lookup/76561198072521779/'
SEARCH_URL = 'https://www.steamidfinder.com/lookup/'


def steam_id_finder(account_id):
    "This method finds the steam32 ID by inputting a normal steam id"
    try:
        # first make our call to request the html of the page
        url = SEARCH_URL + str(account_id)
        response = requests.get(url).text

        # initiate our html parser
        soup = BeautifulSoup(response, "html.parser")

        # find the returns of the search and retrieve the second one (steamID32)
        returns = soup.find_all('code')
        steam_id_32 = returns[1].string

        # string manipulation to retrieve the part we need
        steam_id_32 = steam_id_32.replace('[', '')
        steam_id_32 = steam_id_32.replace(']', '')
        steam_id_32 = steam_id_32.split(':')[2]

        return steam_id_32

    except Exception as e:
        return False

#print(steam_id_finder(76561198072521779))
