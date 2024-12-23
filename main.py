import requests
import pandas as pd
import config

API_KEY = config.api_key
#Function to get player puuid, given a summoner name and region

SUMMONER_URL = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/"
MATCH_URL = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/"
MATCH_DETAILS_URL = "https://americas.api.riotgames.com/tft/match/v1/matches/"
ACCOUNT_URL = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"

def get_account(gameName, tagLine = "NA1"):
    url = f"{ACCOUNT_URL}{gameName}/{tagLine}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_summoner_data(summoner_name):
    url = f"{SUMMONER_URL}{summoner_name}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
# Example Usage
account = get_account(gameName="Tungtwister",tagLine="Tung")
print(account.get("puuid"))
