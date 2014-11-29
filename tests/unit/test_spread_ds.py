from models.datastore.spread_ds import SpreadModel
from random import randint
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

class TestSpread(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def _generate_data(self, year=2014, week=0, count=1):
        game_id = randint(1000, 9000)
        result = []

        for i in range(count):
            data = {
                'game_id': game_id+count,
                'game_line': randint(35, 55) + 0.5,
                'game_odds': randint(-7, 7) + 0.5,
                'week': week,
                'year': year
            }
            result.append(data)

        return result

    def _generate_models(self, year=2014, week=0, count=1):
        test_data = self._generate_data(year=year, week=week, count=count)

        result = []
        for game in test_data:
            spread = SpreadModel(**game)
            result.append(spread)

        return result


    def _prepopulate_datastore(self, year=2014, week=0, count=1):
        ancestor_key = ndb.Key('year', year, 'week', week)
        data = self._generate_data(year=year, week=week, count=count)

        for game in data:
            # Decorate data with ancestor key
            spread_data = {
                'parent': ancestor_key
            }
            spread_data.update(game)

            SpreadModel(**spread_data).put()

        return data

    def test_basic(self):
        week = 5
        year = 2014
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
