import json
from models.datastore.spread_ds import SpreadModel
import main
from random import randint
import unittest
import webtest

class TestSpread(unittest.TestCase):
    def setUp(self):
        self.app = webtest.TestApp(main.application)


    def generate_spread_data(self, year=2014, week=0, count=1):
        ancestor_key = SpreadModel()._generate_key(year=year, week=week)
        result = self._random_spread_data(year=year, week=week, count=count)

        # Load the games into the datastore
        for game in result:
            # parent key is supposed to be transient
            game_data = {
                'parent': ancestor_key
            }
            game_data.update(game)
            SpreadModel(**game_data).put()

        return result


    def _random_spread_data(self, year=2014, week=0, count=1):
        game_id = randint(1000, 9000)
        result = []

        for i in range(count):
            data = {
                'game_id': game_id + count,
                'game_line': randint(39, 55) + 0.5,
                'game_odds': randint(-7, 7) + 0.5,
                'week': week,
                'year': year
            }
            result.append(data)

        return result


    def test_spread_fetch_week_basic(self):
        year = 2014
        week = randint(1, 17)
        endpoint = '/api/v1/spread/year/{0}/week/{1}'.format(year, week)
        test_data = self.generate_spread_data(year=year, week=week)

        response = self.app.get(endpoint)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')

        data = json.loads(response.body)
        self.assertEqual(len(data['spread']), 1)
        for index, game in enumerate(data['spread']):
            expected_game = test_data[index]
            self.assertEqual(game, expected_game)