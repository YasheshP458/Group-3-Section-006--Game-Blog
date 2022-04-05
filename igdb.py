"""
IGDB Movie Data & API Query
Nathan Heckman
"""

import os
import json
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # Find the hidden .env file in directory
client_id = os.getenv("client_id")  # Load IGDB client ID (used for API call)
client_secret = os.getenv("client_secret")  # Load IGDB Client Secret Key
access_token = os.getenv("access_token")  # Load IGDB API Access Token (used for API call)

# Access Token: Listed in .env
# Expires: around June 8, 2022 
# Token Type: bearer


def get_igdb_token_json():
    """
    DO NOT RUN UNLESS TOKEN IS EXPIRED OR NOT WORKING!

    Used to get a new token from API in case of token expiration.
    Not intended to be used outside of this file.
    New token will have to be manually changed in .env (access_token)
    """
    base_url = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"

    # Create the HTTP request
    response = requests.post(base_url)

    # Returns Python dictionary
    game_data = response.json()

    # Print JSON neatly (must add print statement)
    return json.dumps(game_data, indent=4, sort_keys=True)


def get_game_data(game_id: int):
    """
    Used to return the movie data for rendering in the application.
    Gets JSON and interprets from site using id associated with every game.
    """
    base_url = "https://api.igdb.com/v4/games"

    headers = {
        "Client-ID": client_id,
        "Authorization": "Bearer " + access_token,
        "Accept": "application/json",
    }

    # Get all available data. Can be changed to only get specific information
    data = f"fields *; where id = {game_id};"

    response = requests.post(base_url, data=data, headers=headers)

    # Returns Python dictionary
    game_data = response.json()

    # Print JSON neatly (must add print statement)
    return json.dumps(game_data, indent=4, sort_keys=True)


def search_game_data(game_name: str):
    """
    Get video game data through IGDB search.
    Gets JSON and interprets from site using closest search result.
    """
    base_url = "https://api.igdb.com/v4/games"

    headers = {
        "Client-ID": client_id,
        "Authorization": "Bearer " + access_token,
        "Accept": "application/json",
    }

    # Get all available data for first result. Can be changed to only get specific information
    data = f'fields *; where slug = "{game_name}"; limit 1;'

    response = requests.post(base_url, data=data, headers=headers)

    # Returns Python dictionary
    game_data = response.json()

    # Print JSON neatly (must add print statement)
    return json.dumps(game_data, indent=4, sort_keys=True)


# These should return the same thing. search_game_data will fail if the title doesn't exist
print(get_game_data(1074))  # Super Mario 64
print(search_game_data("super-mario-64"))
