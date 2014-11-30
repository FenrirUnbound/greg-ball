import json
import unittest
import webtest
from random import randint

from google.appengine.ext import testbed

import main
from models.datastore.spread_ds import SpreadModel
from models.spread import Spread

class TestSpreadsHandler(unittest.TestCase):
    def setUp(self):
        self.app = webtest.TestApp(main.application)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

        self.year = 2014
        self.week = randint(1, 17)

    def tearDown(self):
        self.testbed.deactivate()


    def generate_spread_data(self, year=2014, week=0, count=1):
        ancestor_key = Spread()._generate_key(year=year, week=week)
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


    def test_fetch_single_by_week(self):
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


    def test_fetch_multiple_by_week(self):
        year = 2014
        week = randint(1, 17)
        count = randint(1, 11)
        endpoint = '/api/v1/spread/year/{0}/week/{1}'.format(year, week)
        test_data = self.generate_spread_data(year=year, week=week, count=count)

        response = self.app.get(endpoint)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')

        data = json.loads(response.body)
        self.assertEqual(len(data['spread']), count)
        for index, game in enumerate(data['spread']):
            expected_game = test_data[index]
            self.assertEqual(game, expected_game)


    def test_save_single_by_week(self):
        year = 2014
        week = randint(1, 17)
        count = 1
        endpoint = '/api/v1/spread/year/{0}/week/{1}'.format(year, week)
        test_data = self._random_spread_data(year=year, week=week, count=count)
        post_body = {
            'spread': json.dumps(test_data)
        }

        response = self.app.put(endpoint, post_body)
        self.assertEqual(response.status_int, 201)

        # Check datastore
        key = Spread()._generate_key(year=year, week=week)
        data = SpreadModel.query(ancestor=key).order(SpreadModel.game_id).fetch(count+1)
        self.assertEqual(len(data), count)

        for index, expected_game in enumerate(test_data):
            game = data[index]
            self.assertEqual(game.to_dict(), expected_game)


    def test_save_multiple_by_week(self):
        count = randint(2, 8)
        endpoint = '/api/v1/spread/year/{0}/week/{1}'.format(self.year, self.week)
        test_data = self._random_spread_data(year=self.year, week=self.week, count=count)
        post_body = {
            'spread': json.dumps(test_data)
        }

        response = self.app.put(endpoint, post_body)
        self.assertEqual(response.status_int, 201)

        # Check datastore
        key = Spread()._generate_key(year=self.year, week=self.week)
        data = SpreadModel.query(ancestor=key).order(SpreadModel.game_id).fetch(count+1)
        self.assertEqual(len(data), count)

        for index, expected_game in enumerate(test_data):
            game = data[index]
            self.assertEqual(game.to_dict(), expected_game)
