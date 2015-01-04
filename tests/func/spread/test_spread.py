import json
import unittest
import webtest
from random import randint

import main
from models.datastore.spread_ds import SpreadModel
from models.spread import Spread

class TestSpreadHandler(unittest.TestCase):
    def setUp(self):
        self.app = webtest.TestApp(main.application)
        self.testbed.init_memcache_stub()
        self.testbed.init_datastore_v3_stub()

        self.year = 2014
        self.week = randint(1, 17)

    def _prepopulate_datastore(self, year=1990, week=0):
        parent_key = Spread()._generate_key(year=year, week=week)
        test_data = self._random_spread_data(year=year, week=week)

        spread_data = {'parent': parent_key}
        spread_data.update(test_data)
        SpreadModel(**spread_data).put()

        return test_data

    def _random_spread_data(self, year=1990, week=0):
        data = {
            'game_id': randint(1000, 9000),
            'game_line': randint(39, 55) + 0.5,
            'game_odds': randint(-7, 7) + 0.5,
            'week': week,
            'year': year
        }
        return data

    def test_fetch(self):
        test_data = self._prepopulate_datastore(year=self.year, week=self.week)
        endpoint = '/api/v1/spread/year/{0}/week/{1}/game/{2}'.format(self.year, self.week, test_data['game_id'])

        response = self.app.get(endpoint)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')

        data = json.loads(response.body)
        self.assertEqual(data, test_data)

    def test_save(self):
        test_data = self._random_spread_data(year=self.year, week=self.week)
        game_id = test_data['game_id']
        endpoint = '/api/v1/spread/year/{0}/week/{1}/game/{2}'.format(self.year, self.week, game_id)
        post_body = {
            'spread': json.dumps(test_data)
        }

        response = self.app.put(endpoint, post_body)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')

        # Check datastore
        data = SpreadModel.query(SpreadModel.game_id == game_id).fetch(1)
        self.assertEqual(data[0].to_dict(), test_data)
