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

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text = True)

            self.assertIn('<table class="board">', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')
            resp = response.get_json()
            gameId = resp['gameId']
            board = resp['board']

            self.assertIsInstance(gameId, str)
            self.assertIsInstance(board, list)
            self.assertIn(gameId, games)

    def test_score_word(self):
        """Test scoring word"""

        with self.client as client:

            # Make api request so we have a game to work with
            new_game_response = client.post('/api/new-game')
            j = new_game_response.get_json()
            game_id = j["gameId"]
            game = games[game_id]

            # Set the game board to something fixed
            game.board = [["C", "A", "T"], ["C", "A", "T"], ["C", "A", "T"]]

            # Check for words in board
            response = client.post('/api/score-word', 
                                   json = {'gameId': game_id , "word" : "CAT"})
            response_json = response.get_json()
            self.assertEqual("ok", response_json['result'])


            # Check for words not on board
            response = client.post('/api/score-word', 
                                   json = {'gameId': game_id , "word" : "DOG"})
            response_json = response.get_json()
            self.assertEqual("not-on-board", response_json['result'])


            # Check for not word
            response = client.post('/api/score-word', 
                                   json = {'gameId': game_id , "word" : "TTT"})
            response_json = response.get_json()
            self.assertEqual("not-word", response_json['result'])




           
