import requests
import os

def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    response = requests.get(url, stream=True)
    file_name = os.path.join(dest_folder, url.split('/')[-1])
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    return file_name

def get_tft_assets(version):
    base_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/"
    assets = {
        "champions": "tft-champion.json",
        "items": "tft-item.json",
        "traits": "tft-trait.json",
        "augments": "tft-augments.json"
    }
    dest_folder = "./assets"
    for asset, file_name in assets.items():
        url = base_url + file_name
        download_file(url, dest_folder)
        print(f"Downloaded {asset} data to {dest_folder}/{file_name}")

if __name__ == "__main__":
    latest_version = "14.24.1"  # Replace with the latest version if needed
    get_tft_assets(latest_version)