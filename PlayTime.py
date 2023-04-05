import json
import requests

def get_game_list():
    # Make a request to the Steam API to get the list of games
    url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
    response = requests.get(url)

    # Check if the response was successful
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        # Extract the list of games and their IDs
        game_list = {}
        for game in data.get('applist', {}).get('apps', []):
            game_list[game['appid']] = game['name']
        return game_list
    else:
        # If the response was unsuccessful, raise an exception
        raise Exception(f'Request failed with status code {response.status_code}')

# Example usage
games = get_game_list()

# Write the game IDs and names to a file
with open('game_list.json', 'w') as f:
    json.dump(games, f, indent=4)

# Print out the number of games in the list
print(f'{len(games)} games written to file.')



GAME_LIST_FILE = 'game_list.json'

def load_game_list():
    with open(GAME_LIST_FILE, 'r') as f:
        game_list = json.load(f)
        # Convert the keys to integers
        return {int(k): v for k, v in game_list.items()}

def save_game_list(game_list):
    # Convert the keys back to strings
    game_list = {str(k): v for k, v in game_list.items()}
    with open(GAME_LIST_FILE, 'w') as f:
        json.dump(game_list, f, indent=4)

def get_game_id(game_name):
    game_list = load_game_list()
    # Search for the game name in the values
    game_id = next((k for k, v in game_list.items() if v == game_name), None)
    if game_id:
        return game_id
    else:
        # If the game is not in the list, add it
        print(f'Game "{game_name}" not found in the list. Adding it to the list.')
        new_id = max(game_list.keys()) + 1
        game_list[new_id] = game_name
        save_game_list(game_list)
        return new_id

def get_playtime(game_id, steam_id):
    # Make a request to the Steam API to get the user's game details
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=<api_key_here>&steamid={steam_id}&format=json'
    response = requests.get(url)

    # Check if the response was successful
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        # Check if the user owns the specified game
        games = data.get('response', {}).get('games', [])
        for game in games:
            if game['appid'] == game_id:
                # Return the playtime for the game in minutes
                return game.get('playtime_forever', 0)
    else:
        # If the response was unsuccessful, raise an exception
        raise Exception(f'Request failed with status code {response.status_code}')

# Example usage
game_name = input('Enter game name: ')
game_id = get_game_id(game_name)
steam_id = input('Enter Steam ID: ')
playtime = get_playtime(game_id, steam_id)
print(f'Playtime for game "{game_name}": {playtime} minutes')


import os
import requests

# Make an API request to retrieve the game name and the user's game achievements
response = requests.get(f'https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key=<api_key_here>A&appid={game_id}')
game_name = response.json()['game']['gameName']

response = requests.get(f'https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={game_id}&key=<api_key_here>A&steamid={steam_id}')

# Parse the API response
data = response.json()['playerstats']

# Check if the achievements file already exists
if os.path.isfile('achievements.txt'):
    # Read the contents of the file
    with open('achievements.txt', 'r') as file:
        contents = file.read()
    # Check if the game already exists in the file
    if game_name in contents:
        # Overwrite the achievements for the game
        with open('achievements.txt', 'w') as file:
            file.write(contents.replace(f"{game_name}\n\n", f"Game Name: {game_name}\n\n"))
            for achievement in data['achievements']:
                if achievement['achieved'] == 1:
                    file.write(f"{achievement['apiname']} - achieved on {achievement['unlocktime']}\n")
                else:
                    file.write(f"{achievement['apiname']} - not yet achieved\n")
    else:
        # Append the game's achievements to the end of the file
        with open('achievements.txt', 'a') as file:
            file.write(f"\nGame Name: {game_name}\n\n")
            for achievement in data['achievements']:
                if achievement['achieved'] == 1:
                    file.write(f"{achievement['apiname']} - achieved on {achievement['unlocktime']}\n")
                else:
                    file.write(f"{achievement['apiname']} - not yet achieved\n")
else:
    # Write the game name and the user's progress towards each achievement to the file
    with open('achievements.txt', 'w') as file:
        file.write(f"Game Name: {game_name}\n\n")
        for achievement in data['achievements']:
            if achievement['achieved'] == 1:
                file.write(f"{achievement['apiname']} - achieved on {achievement['unlocktime']}\n")
            else:
                file.write(f"{achievement['apiname']} - not yet achieved\n")

# Print a message to indicate that the data has been saved to the file
print("Achievement data has been saved to the file 'achievements.txt'")


