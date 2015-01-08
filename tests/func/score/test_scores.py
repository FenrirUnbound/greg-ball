from __future__ import unicode_literals


import json
import unittest
import webtest
from random import randint

from google.appengine.ext import ndb

import main
from models.datastore.score_ds import ScoreModel

class TestScoresHandler(unittest.TestCase):
    def setUp(self):
        self.app = webtest.TestApp(main.application)
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        self.year = 2014
        self.week = randint(1, 17)

    def _score_data_final(self):
        result = []
        with open('tests/data/reg.json') as data_file:
            result = json.load(data_file)
        return result

    def _postseason_score_data(self):
        result = []
        with open('tests/data/post.json') as data_file:
            result = json.load(data_file)
        return result

    def _load_datastore(self, year, week, data):
        parent_key = ndb.Key('year', year, 'week', week)
        to_save = []
        for game in data:
            item = {'parent': parent_key}
            item.update(game)
            score = ScoreModel(**item)
            to_save.append(score)
        ndb.put_multi(entities=to_save)

    def _remove_invalids(self, data):
        result = []
        for game in data:
            if game['game_id'] > 0:
                result.append(game)
        return result

    def test_fetch(self):
        endpoint = '/api/v1/score/year/{0}/week/{1}'.format(self.year, self.week)
        test_data = self._score_data_final()

        self._load_datastore(year=self.year, week=self.week, data=test_data)

        response = self.app.get(endpoint)
        self.assertEqual(response.status_int, 200)

        data = json.loads(response.body)
        self.assertEqual(len(data), len(test_data))
        self.assertEqual(data, test_data)

    def test_fetch_postseason(self):
        self.week = 18
        endpoint = '/api/v1/score/year/{0}/week/{1}'.format(self.year, self.week)
        test_data = self._postseason_score_data()

        self._load_datastore(year=self.year, week=self.week, data=test_data)
        # Need to load the invalid data, but filter it for the test assertion
        test_data = self._remove_invalids(data=test_data)

        response = self.app.get(endpoint)
        self.assertEqual(response.status_int, 200)

        data = json.loads(response.body)
        self.assertEqual(len(data), len(test_data))
        self.assertEqual(data, test_data)

    def test_fetch_nothing(self):
        endpoint = '/api/v1/score/year/{0}/week/{1}'.format(self.year, self.week)

        response = self.app.get(endpoint)
        self.assertEqual(response.status_int, 200)

        data = json.loads(response.body)
        self.assertEqual(len(data), 0)
