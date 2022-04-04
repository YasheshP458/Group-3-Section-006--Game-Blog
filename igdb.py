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


# Example query for getting all available data for 10 games (default)
def get_game_data():
    """
    Used to return the movie data for rendering in the application.
    Gets JSON and interprets from site.
    """

    base_url = "https://api.igdb.com/v4/games/"

    headers = {
        "Client-ID": client_id,
        "Authorization": "Bearer " + access_token,
    }

    # Get all available data. Can be changed to only get specific information
    data = "fields *;"

    response = requests.post(base_url, data=data, headers=headers)

    # Returns Python dictionary
    game_data = response.json()

    # Print JSON neatly (must add print statement)
    return json.dumps(game_data, indent=4, sort_keys=True)


print(get_game_data())

"""
Example Code from Milestone if needed.
Can use this similar logic to pass specific variables to our app.

def get_title(game_data):
    return game_data["title"]

def get_tagline(game_data):
    return game_data["tagline"]

def get_genres(game_data):
    genre_data = game_data["genres"]
    genres = []
    for i in range(len(genre_data)):
        genre_data = game_data["genres"][i]["name"]
        genres.append(genre_data)
    return genres

def get_poster(game_data):
    return game_data["poster_path"]

title = get_title(game_data)
tagline = get_tagline(game_data)
genres = get_genres(game_data)
poster = get_poster(game_data)

# Lists or values to be passed to application. Single movie
return title, tagline, genres, poster
"""
