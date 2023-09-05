import requests
import pandas as pd
import config

api_key = config.api_key
#Function to get player puuid, given a summoner name and region
def get_puuid(summoner_name, region, api_key):
    api_url = (
        "https://" +
        region +
        ".api.riotgames.com/tft/summoner/v1/summoners/by-name/" +
        summoner_name +
        "?api_key=" +
        api_key
    )

    print(api_url)
    resp = requests.get(api_url)
    player_info = resp.json()
    puuid = player_info['puuid']
    return puuid

#Function to get a list of all the match IDs, given a players puuid and mass region
#totaling 20 match IDs
def get_match_ids(puuid, mass_region, api_key):
    api_url = (
        "https://" +
        mass_region +
        ".api.riotgames.com/tft/match/v1/matches/by-puuid/" +
        puuid + 
        "/ids?start=0&count=20" + 
        "&api_key=" + 
        api_key
    )
    
    print(api_url)
    
    resp = requests.get(api_url)
    match_ids = resp.json()
    return match_ids


# From a given match ID and mass region, get the data about the game
def get_match_data(match_id, mass_region, api_key):
    api_url = (
        "https://" + 
        mass_region + 
        ".api.riotgames.com/tft/match/v1/matches/" +
        match_id + 
        "?api_key=" + 
        api_key
    )
    
    resp = requests.get(api_url)
    match_data = resp.json()
    return match_data


def gather_all_data(puuid, match_ids, mass_region, api_key):
    # We initialise an empty dictionary to store data for each game
    data = {
        'traits': [],

    }
    
    for match_id in match_ids:
        print(match_id)
        # run the two functions to get the player data from the   match ID
        match_data = get_match_data(match_id, mass_region, api_key)
        print(match_data[traits])
 
puuid = get_puuid("Leáf", "na1", api_key)
match_ids = get_match_ids(puuid, "AMERICAS", api_key)
print(match_ids)
get_match_data(match_ids[0], "AMERICAS", api_key)