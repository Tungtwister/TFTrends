import requests
import pandas as pd
import config

API_KEY = config.api_key
#Function to get player puuid, given a summoner name and region

ACCOUNT_URL = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
MATCH_URL = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/"
MATCH_DETAILS_URL = "https://americas.api.riotgames.com/tft/match/v1/matches/"

def get_account(gameName, tagLine = "NA1"):
    url = f"{ACCOUNT_URL}{gameName}/{tagLine}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_match_ids(puuid, start=0, count=20):
    url = f"{MATCH_URL}{puuid}/ids?start={start}&count={count}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Returns a list of match IDs
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
def get_match_details(match_id):
    url = f"{MATCH_DETAILS_URL}{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_player_metadata(match_details, player_puuid):
    if not match_details:
        print("No match details provided.")
        return None

    # Get the list of participants
    participants = match_details.get("info", {}).get("participants", [])
    
    # Find the participant matching the player's PUUID
    for participant in participants:
        if participant.get("puuid") == player_puuid:
            return participant  # Return the metadata for this player

    print(f"Player with PUUID {player_puuid} not found in this match.")
    return None

def transform_match_data(match_data, player_puuid):
    rows = []
    participants = match_data["info"]["participants"]
    for participant in participants:
        if participant.get("puuid") == player_puuid:
            row = {
                "placement": participant["placement"],
                "level": participant["level"],
                "gold_left": participant["gold_left"],
                "time_eliminated": participant["time_eliminated"],
                "last_round": participant["last_round"],
                "total_damage_to_players": participant.get("total_damage_to_players", 0),
                "num_traits": len(participant["traits"]),
                "num_units": len(participant["units"]),
                # Extract trait data (example: Bruiser, Sorcerer)
                **{trait["name"]: trait["num_units"] for trait in participant["traits"]},

            }

             # Extract unit data
            for i, unit in enumerate(participant["units"]):
                unit_key = f"unit_{i+1}"
                row[f"{unit_key}_name"] = unit["character_id"]  # Unit name
                row[f"{unit_key}_tier"] = unit["tier"]  # Unit star/tier level
                row[f"{unit_key}_items"] = ",".join(map(str, unit["itemNames"]))  # List of item IDs as a string

            rows.append(row)
    return rows

def build_dataset(puuid, start=0, count=20):
    match_ids = get_match_ids(puuid, start, count)
    dataset = []
    for match_id in match_ids:
        match_data = get_match_details(match_id)
        if match_data:
            dataset.extend(transform_match_data(match_data, puuid))
    return pd.DataFrame(dataset)

account = get_account(gameName="Tungtwister",tagLine="Tung")
puuid = account.get("puuid")

df = build_dataset(puuid, start=0, count=20)
df.to_csv("tft_dataset.csv", index=False)
print(df)
