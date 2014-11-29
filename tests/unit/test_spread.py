from random import randint
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from models.datastore.spread_ds import SpreadModel
from models.spread import Spread


class TestSpread(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

        self.year = 2014
        self.week = randint(1, 17)

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

    def test_generate_key(self):
        expected_key = ndb.Key('year', self.year, 'week', self.week)
        key = Spread()._generate_key(year=self.year, week=self.week)
        self.assertEqual(key, expected_key)

    def test_save_spread(self):
        year = 2014
        week = randint(1, 17)
        expected_count = 1
        test_data = self._generate_data(year=year, week=week, count=expected_count)

        spread = Spread()
        count = spread.save(year=year, week=week, data=test_data)
        self.assertEqual(count, expected_count)

        # Check datastore
        ancestor_key = SpreadModel.generate_key(year=year, week=week)
        data = SpreadModel().query(ancestor=ancestor_key).order(SpreadModel.game_id).fetch(expected_count+1)
        self.assertEqual(len(data), expected_count)

        for index in range(expected_count):
            expected_game = test_data[index]
            game = data[index].to_dict()
            self.assertEqual(game, expected_game)

    def test_save_multiple_spread(self):
        expected_count = randint(2, 16)
        test_data = self._generate_data(year=self.year, week=self.week, count=expected_count)

        spread = Spread()
        count = spread.save(year=self.year, week=self.week, data=test_data)
        self.assertEqual(count, expected_count)

        # Check datastore
        ancestor_key = spread._generate_key(year=self.year, week=self.week)
        data = SpreadModel().query(ancestor=ancestor_key).order(SpreadModel.game_id).fetch(expected_count+1)
        self.assertEqual(len(data), expected_count)

        for index in range(expected_count):
            expected_game = test_data[index]
            game = data[index].to_dict()
            self.assertEqual(game, expected_game)


