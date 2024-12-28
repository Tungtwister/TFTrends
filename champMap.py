import json
import pandas as pd

def champCost():
    # Load JSON data from a file
    with open('assets/tft-champion.json', 'r') as file:
        data = json.load(file)

    champion_mapping = {
        value["id"]: {
            "name": value["name"],
            "cost": value["tier"]
        }
        for key, value in data["data"].items()
    }

    # Create a DataFrame
    df = pd.DataFrame(champion_mapping).T

    # Filter the DataFrame to get only tft13 champions
    tft13_champions = df[df.index.str.startswith('TFT13_')]
    return tft13_champions

