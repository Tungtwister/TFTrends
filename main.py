import requests
import pandas as pd
import config
import champMap

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

#General Stats
games_played = len(df)
avg_placement = df["placement"].mean()
avg_level = df["level"].mean()
avg_gold_left = df["gold_left"].mean()
avg_time_eliminated = df["time_eliminated"].mean()
avg_last_round = df["last_round"].mean()
avg_total_damage_to_players = df["total_damage_to_players"].mean()

print(f"Games Played: {games_played}")
print(f"Avg Placement: {avg_placement}")
print(f"Avg Level: {avg_level}")
print(f"Avg Gold Left: {avg_gold_left}")
print(f"Avg Time Eliminated: {avg_time_eliminated}")
print(f"Avg Last Round: {avg_last_round}")
print(f"Avg Total Damage to Players: {avg_total_damage_to_players}")

df["top4"] = df["placement"] <= 4
top4_rate = df["top4"].mean() * 100
win_rate = df["placement"].eq(1).mean() * 100
avg_star_level = df.filter(regex=r"unit_\d+_tier").mean().mean()

print(f"Top 4 Rate: {top4_rate:.2f}%")
print(f"Win Rate: {win_rate:.2f}%")
print(f"Avg Star Level: {avg_star_level:.2f}")


# Load the champion cost data
champ_cost_df = champMap.champCost()

# Calculate the total cost of a team for each match
def calculate_team_cost(row, champ_cost_df):
    total_cost = 0
    for i in range(1, row["level"] + 1):  # Iterate from 1 to the player's level at the end of the game
        unit_name = row.get(f"unit_{i}_name")
        unit_tier = row.get(f"unit_{i}_tier")
        if unit_name:
            unit_name = unit_name.lower()
            unit_cost = champ_cost_df.get(unit_name, 0)
            total_cost += unit_cost * (3 ** (unit_tier - 1))
    return total_cost

# Apply the function to each row in the DataFrame
df["team_cost"] = df.apply(calculate_team_cost, champ_cost_df=champ_cost_df, axis=1)
# Calculate average team cost
avg_team_cost = df["team_cost"].mean()
print(f"Avg Team Cost: {avg_team_cost:.2f}")