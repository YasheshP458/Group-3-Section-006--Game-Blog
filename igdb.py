"""
IGDB Movie Data & API Query
Nathan Heckman
"""

#pylint: disable=line-too-long, invalid-name, pointless-string-statement

from inspect import cleandoc
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
    game_name = clean_string(game_name)

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

    game_id = game_data[0]['id']
    game_name = game_data[0]['name']
    game_summary = game_data[0]['summary']

    cover_url = get_cover_url(game_id)

    # Return the game information needed. Can be assigned via tuple in app.py
    return game_name, cover_url, game_summary

def get_cover_url(game_id: int):
    """
    Gets the cover art for a specific game based on its game ID.
    """
    base_url = "https://api.igdb.com/v4/covers"

    headers = {
        "Client-ID": client_id,
        "Authorization": "Bearer " + access_token,
        "Accept": "application/json",
    }

    # Get the specific URL for that game's thumbnail cover image
    data = f'fields url; where game = {game_id};'

    response = requests.post(base_url, data=data, headers=headers)

    # Returns Python dictionary with cover data
    cover_data = response.json()

    # Get the thumbnail version of the image fro JSON response
    image_url = cover_data[0]['url']

    # Get only the specific image file name
    image_file = image_url[44:]

    # Gets the larger version of the picture. Not sure how to access natively
    image_url = "//images.igdb.com/igdb/image/upload/t_cover_big/" + image_file

    # Return cleaned image URL
    return image_url

def clean_string(s: str):
    """
    Trim and clean user input string for processing in search_game_data()
    """
    # 1. Trim whitespace from front and back of string
    # 2. Convert string to lowercase
    # 3. Replace all remaining spaces with dash

    """ Super Mario 64 --> super-mario-64 """

    return s.strip().lower().replace(" ", "-")

'''Example Use Cases'''

''' print(get_game_data(1074))  <-- Generate data for Super Mario 64 based on Game ID '''
''' print(search_game_data("super-mario-strikers")) <-- Input must be formatted in this way for slug search to work. Returns game title, cover art url, and summary currently '''
''' print(get_cover_url(2256)) <-- Used within search_game_data(). This example generates the cover art for Super Mario Strikers '''

''' Note that search_game_data() will fail if that exact game slug doesn't exist. The slug for most games is just their name hyphenated as a single word, so this shouldn't be much of an issue. '''
''' User input will have to be altered so that the input to search_game_data() is lower-case, trailing white space is erased, and each word is seperated with hyphens. '''