import json
import unittest
import webtest
from random import randint

from google.appengine.ext import ndb

import main
from models.datastore.score_ds import ScoreModel
from models.score import Score

class TestScoreHandler(unittest.TestCase):
    def setUp(self):
        self.app = webtest.TestApp(main.application)
        self.testbed.init_memcache_stub()
        self.testbed.init_datastore_v3_stub()

        self.year = 2014
        self.week = randint(1, 17)

    def generate_score_data(self, year=1990, week=0):
        test_data = self._random_test_data(year=year, week=week)
        key = Score()._generate_key(game_id=test_data['game_id'], week=week, year=year)

        data = {'key': key}
        data.update(test_data)
        ScoreModel(**data).put()

        return test_data

    def _random_test_data(self, year=1990, week=0):
        data = {
            'away_name': None,
            'away_score': randint(0, 99),
            'game_clock': '00:00',
            'game_day': 'Sun',
            'game_id': randint(1000, 9000),
            'game_status': 'Final',
            'game_time': '{0}{1}:{2}{3}'.format(randint(0, 2), randint(0, 9), randint(0, 6), randint(0, 9)),
            'home_name': None,
            'home_score': randint(0, 99),
            'week': week,
            'year': year
        }
        return data

    def test_fetch_game(self):
        test_data = self.generate_score_data(year=self.year, week=self.week)
        game_id = test_data['game_id']
        endpoint = '/api/v1/score/year/{0}/week/{1}/game/{2}'.format(self.year, self.week, game_id)

        response = self.app.get(endpoint)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')

        data = json.loads(response.body)
        self.assertEqual(data, test_data)

    def test_save_game(self):
        test_data = self._random_test_data(year=self.year, week=self.week)
        game_id = test_data['game_id']
        endpoint = '/api/v1/score/year/{0}/week/{1}/game/{2}'.format(self.year, self.week, game_id)
        post_data = {
            'game': json.dumps(test_data)
        }

        response = self.app.put(endpoint, post_data)
        self.assertEqual(response.status_int, 200)

        # Check datastore
        data = ScoreModel.query(ScoreModel.game_id == game_id).fetch(2)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].to_dict(), test_data)

    def test_save_same_game_performs_update(self):
        test_data = self._random_test_data(year=self.year, week=self.week)
        game_id = test_data['game_id']
        endpoint = '/api/v1/score/year/{0}/week/{1}/game/{2}'.format(self.year, self.week, game_id)
        post_data = {
            'game': json.dumps(test_data)
        }

        self.app.put(endpoint, post_data)

        # update data
        test_data['home_score'] += 14
        post_data = {
            'game': json.dumps(test_data)
        }

        response = self.app.put(endpoint, post_data)
        self.assertEqual(response.status_int, 200)

        # Check datastore
        data = ScoreModel.query(ScoreModel.game_id == game_id).fetch(2)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].to_dict(), test_data)
