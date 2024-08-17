import requests

API_KEY = 'your_api_key_here'
BASE_URL = 'https://api-nba-v1.p.rapidapi.com'

headers = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': 'api-nba-v1.p.rapidapi.com'
}

def get_seasons():
    response = requests.get(f"{BASE_URL}/seasons/", headers=headers)
    return response.json()

def fetch_player_data():
    response = requests.get(f"{BASE_URL}/players", headers=headers)
    if response.status_code == 200:
        return response.json()['players']
    else:
        return []

# Example: Fetch data for a specific player
def fetch_player_by_id(player_id):
    response = requests.get(f"{BASE_URL}/players/id/{player_id}", headers=headers)
    if response.status_code == 200:
        return response.json()['player']
    else:
        return None
