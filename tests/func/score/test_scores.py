from __future__ import unicode_literals

import json
import mock
import unittest
import webtest
from random import randint

from google.appengine.api import urlfetch
from google.appengine.ext import ndb


import main
from models.datastore.score_ds import ScoreModel

class TestScoresHandler(unittest.TestCase):
    def setUp(self):
        self.app = webtest.TestApp(main.application)
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_urlfetch_stub()

        self.year = 2014
        self.week = randint(1, 17)

    def _create_mock(self, content=''):
        class UrlMock(object):
            def __init__(self):
                self.content = content
        return UrlMock()

    def _score_data_string(self):
        result = '{"ss":[["Thu","12:30","Final",,"CHI","17","DET","34",,,"56346",,"REG13","2014"],'
        result += '["Thu","4:30","Final",,"PHI","33","DAL","10",,,"56347",,"REG13","2014"],'
        result += '["Thu","8:30","Final",,"SEA","19","SF","3",,,"56348",,"REG13","2014"],'
        result += '["Sun","1:00","Pregame",,"SD",,"BAL",,,,"56349",,"REG13","2014"],'
        result += '["Sun","1:00","Pregame",,"CLE",,"BUF",,,,"56350",,"REG13","2014"],'
        result += '["Sun","1:00","Pregame",,"TEN",,"HOU",,,,"56351",,"REG13","2014"],'
        result += '["Sun","1:00","Pregame",,"WAS",,"IND",,,,"56352",,"REG13","2014"],'
        result += '["Sun","1:00","Pregame",,"NYG",,"JAC",,,,"56353",,"REG13","2014"],'
        result += '["Sun","1:00","Pregame",,"CAR",,"MIN",,,,"56354",,"REG13","2014"],'
        result += '["Sun","1:00","Pregame",,"NO",,"PIT",,,,"56355",,"REG13","2014"],'
        result += '["Sun","1:00","Pregame",,"OAK",,"STL",,,,"56356",,"REG13","2014"],'
        result += '["Sun","1:00","Pregame",,"CIN",,"TB",,,,"56357",,"REG13","2014"],'
        result += '["Sun","4:05","Pregame",,"ARI",,"ATL",,,,"56358",,"REG13","2014"],'
        result += '["Sun","4:25","Pregame",,"NE",,"GB",,,,"56359",,"REG13","2014"],'
        result += '["Sun","8:30","Pregame",,"DEN",,"KC",,,,"56360",,"REG13","2014"],'
        result += '["Mon","8:30","Pregame",,"MIA",,"NYJ",,,,"56361",,"REG13","2014"]]}'
        return result

    def _score_data_final(self):
        result = [
            {
                'away_name': 'CHI',
                'away_score': 17,
                'game_clock': '00:00',
                'game_day': 'Thu',
                'game_id': 56346,
                'game_status': 'Final',
                'game_time': '12:30',
                'home_name': 'DET',
                'home_score': 34,
                'week': 13,
                'year': 2014
            }
        ]
        return result

    @mock.patch('models.score.urlfetch')
    def test_fresh_fetch(self, mock_urlfetch):
        expected_count = 16
        endpoint = '/api/v1/score/year/{0}/week/{1}'.format(self.year, self.week)
        mock_urlfetch.fetch.return_value = self._create_mock(self._score_data_string())

        response = self.app.get(endpoint)
        self.assertEqual(response.status_int, 200)

        data = json.loads(response.body)
        self.assertEqual(len(data), expected_count)
        self.assertEqual(data[0], self._score_data_final()[0])
