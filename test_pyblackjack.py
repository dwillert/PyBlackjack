from unittest import TestCase
from mock import patch
from pyblackjack import Deck, GameOptions

class TestPyBlackJack(TestCase):
    def test_score_check_ace(self):
        game_client = GameOptions()
        game_client.player_hand = [{'suit': 'Club', 'value': '10'}, {'suit': 'Heart', 'value': 'A'}]
        retval = game_client.score_check()