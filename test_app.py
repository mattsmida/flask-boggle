from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            ...
            # test that you're getting a template
            self.assertIn('<title>Boggle</title>', html)
            #could also look for test-specific comment in html

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:
            response = client.post('/api/new-game')
            response_json = response.get_json()

            #make sure json has right keys
            self.assertIn("game_id", response_json)
            self.assertIn("board", response_json)

            #make sure values are right types
            self.assertIsInstance(response_json['game_id'], str)
            self.assertIsInstance(response_json['board'], list)
            self.assertIsInstance(response_json['board'][0], list)

            #make sure games is populated with the game we got back
            self.assertTrue(games[response_json['game_id']])