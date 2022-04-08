"""
IGDB Movie Data & API Query Unit Tests
Aaron Reyes
"""

import unittest
from unittest.mock import MagicMock, patch
from igdb import (
    get_igdb_token_json,
    get_game_data,
    search_game_data,
    get_cover_url,
    clean_string,
)


class IgdbTests(unittest.TestCase):
    def test_get_igdb_token_json(self):
        """
        Tests a function used to get a new token from API in case of token expiration.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        with patch("igdb.requests.get") as mock_get:
            mock_get.return_value = mock_response
            result = get_igdb_token_json()
            self.assertEqual(result, "google.com")

    def test_get_game_data(self):
        """
        Tests a function used to return the game data for rendering in the application.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        with patch("igdb.requests.get") as mock_get:
            mock_get.return_value = mock_response
            result = get_game_data(1074)
            self.assertEqual(result, "google.com")

    def test_search_game_data(self):
        """
        tests a function used to get video game data through IGDB search.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        with patch("igdb.requests.get") as mock_get:
            mock_get.return_value = mock_response
            result = search_game_data("Super Mario Strikers")
            self.assertEqual(result, ('Super Mario Strikers', '//images.igdb.com/igdb/image/upload/t_cover_big/co1xd3.jpg', 'Forget what you know about soccer, because in the Mushroom Kingdom, anything goes! Get ready for crazy five-on-five matches as Mario and Co. hit the pitch for the first time ever!'))

    def test_get_cover_url(self):
        """
        tests function that gets the cover art for a specific game based on its game ID.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        with patch("igdb.requests.get") as mock_get:
            mock_get.return_value = mock_response
            result = get_cover_url(2256  )
            self.assertEqual(result, "//images.igdb.com/igdb/image/upload/t_cover_big/co1xd3.jpg")


    def test_clean_string(self):
        """
        tests a function to trim and clean user input string for processing in search_game_data()
        """   
        result = clean_string("Super Mario 64")
        self.assertEqual(result, "super-mario-64")


if __name__ == "__main__":
    unittest.main()
