import unittest
from random import randint

from google.appengine.ext import ndb

from models.datastore.spread_ds import SpreadModel

class TestSpread(unittest.TestCase):
    def setUp(self):
        self.testbed.init_memcache_stub()
        self.testbed.init_datastore_v3_stub()


    def test_basic(self):
        year = 2014
        week = randint(1, 17)
        test_key = ndb.Key('week', week)
        data = [
            {
                'parent': test_key,
                'game_id': 123,
                'game_line': 42.5,
                'game_odds': -3.5,
                'week': week,
                'year': year
            },
            {
                'parent': test_key,
                'game_id': 125,
                'game_line': 37.5,
                'game_odds': 1.5,
                'week': week,
                'year': year
            },
            {
                'parent': test_key,
                'game_id': 130,
                'game_line': 50.5,
                'game_odds': -7.5,
                'week': week,
                'year': year
            }
        ]

        for game in data:
            SpreadModel(**game).put()

        query = SpreadModel.query(ancestor=test_key).order(-SpreadModel.game_id)
        result = query.fetch(10)

        self.assertEqual(len(result), 3)
        for index, game in enumerate(reversed(data)):
            self.assertEqual(result[index].game_id, game['game_id'])
