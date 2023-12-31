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
            self.assertTrue(games[response_json['game_id']]) #assertIn

    def test_api_score_word(self):
        """ Test whether score word function checks for word in dictionary,
            presence on board (does not check word length!).
            Uses new-game api to set up the game first."""

        with app.test_client() as client:

            get_game_response = client.post('/api/new-game')
            get_game_response_dict = get_game_response.get_json()

            game_id = get_game_response_dict['game_id']
            game = games[game_id]

            game.board = [
                ['C','A','T','C','A'],
                ['C','A','T','C','A'],
                ['C','A','T','C','A'],
                ['C','A','T','C','A'],
                ['C','A','T','C','A']
            ]

            json_cat = { 'game_id': game_id, 'word': 'cat' }
            json_CAT = { 'game_id': game_id, 'word': 'CAT' }
            json_FISH = { 'game_id': game_id, 'word': 'FISH' }
            json_AAAAA = { 'game_id': game_id, 'word': 'AAAAA' }

            response_cat = client.post('/api/score-word', json=json_cat)
            response_cat_dict = response_cat.get_json()
            self.assertEqual(response_cat_dict['result'], 'not-word')

            response_CAT = client.post('/api/score-word', json=json_CAT)
            response_CAT_dict = response_CAT.get_json()
            self.assertEqual(response_CAT_dict['result'], 'ok')

            response_FISH = client.post('/api/score-word', json=json_FISH)
            response_FISH_dict = response_FISH.get_json()
            self.assertEqual(response_FISH_dict['result'], 'not-on-board')

            response_AAAAA = client.post('/api/score-word', json=json_AAAAA)
            response_AAAAA_dict = response_AAAAA.get_json()
            self.assertEqual(response_AAAAA_dict['result'], 'not-word')














