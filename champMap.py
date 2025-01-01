import json
import pandas as pd

def champCost():
    # Load JSON data from a file
    with open('assets/tft-champion.json', 'r') as file:
        data = json.load(file)

    champion_mapping = {
        value["id"]: {
            "name": value["id"].lower(),
            "cost": value["tier"]
        }
        for key, value in data["data"].items()
    }

    # Create a DataFrame
    df = pd.DataFrame(champion_mapping).T
    # Filter the DataFrame to get only tft13 champions
    tft13_champions = df[df.index.str.startswith('TFT13_')]

    tft13_champions_dict = tft13_champions.set_index('name')['cost'].to_dict()
    return tft13_champions_dict


