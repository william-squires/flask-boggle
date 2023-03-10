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

    # def test_score_word(self):
    #     """Test scoring word"""

    #     with self.client as client:
    #         response = client.post('/api/score-word', 
    #                                json = {'gameId':})





           
