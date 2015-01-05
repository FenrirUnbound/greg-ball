import json
import mock
import unittest
import webtest

import main
from models.datastore.score_ds import ScoreModel

class TestCronScoreHandler(unittest.TestCase):
    def setUp(self):
        self.app = webtest.TestApp(main.application)
        self.testbed.init_memcache_stub()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_urlfetch_stub()

        self.year = 2014

    def _create_mock(self, content=''):
        class UrlMock(object):
            def __init__(self):
                self.content = content
        return UrlMock()

    def _score_postseason(self):
        result = '{"ss":[["Sat","8:15","4","02:57","Baltimore Ravens","BAL","30","Pittsburgh Steelers","PIT","15","BAL","0","56492","INT","NBC","POST18","2014"],'
        result += '["Sat","4:35","Final",,"Arizona Cardinals","ARI","16","Carolina Panthers","CAR","27",,,"56491",,"ESPN","POST18","2014"],'
        result += '["Sun","1:05","Pregame",,"Cincinnati Bengals","CIN",,"Indianapolis Colts","IND",,,,"56493",,"CBS","POST18","2014"],'
        result += '["Sun","4:40","Pregame",,"Detroit Lions","DET",,"Dallas Cowboys","DAL",,,,"56494",,"FOX","POST18","2014"],'
        result += '["Jan 10","4:35","Pregame",,,"TBD",,"New England Patriots","NE",,,,"0",,"NBC","POST18","2014"],'
        result += '["Jan 10","8:15","Pregame",,,"TBD",,"Seattle Seahawks","SEA",,,,"0",,"FOX","POST18","2014"],'
        result += '["Jan 11","1:05","Pregame",,,"TBD",,"Green Bay Packers","GB",,,,"0",,"FOX","POST18","2014"],'
        result += '["Jan 11","4:40","Pregame",,,"TBD",,"Denver Broncos","DEN",,,,"0",,"CBS","POST18","2014"],'
        result += '["Jan 18","3:05","Pregame",,,"TBD",,,"TBD",,,,"0",,"FOX","POST18","2014"],'
        result += '["Jan 18","6:40","Pregame",,,"TBD",,,"TBD",,,,"0",,"CBS","POST18","2014"],'
        result += '["Jan 25","8:00","Pregame",,,"TBD",,,"TBD",,,,"0",,"ESPN","POST18","2014"],'
        result += '["Feb 1","6:30","Pregame",,,"TBD",,,"TBD",,,,"0",,"NBC","POST18","2014"]]}'
        return result

    def _score_data_postseason(self):
        result = [
            {
                'away_name': 'BAL',
                'away_score': 30,
                'game_clock': '02:57',
                'game_day': 'Sat',
                'game_id': 56492,
                'game_status': '4',
                'game_time': '8:15',
                'home_name': 'PIT',
                'home_score': 15,
                'week': 18,
                'year': 2014
            }
        ]
        return result

    @mock.patch('models.scoreboard.urlfetch')
    def test_fresh_fetch_postseason(self, mock_urlfetch):
        expected_count = 12
        expected_url = 'http://www.nfl.com/liveupdate/scorestrip/postseason/scorestrip.json'
        expected_week = 18      # Postseason data is defaulted to week 18 with "POST18" tag
        endpoint = '/api/v1/cron/score/latest'
        mock_urlfetch.fetch.return_value = self._create_mock(self._score_postseason())

        response = self.app.post(endpoint)
        self.assertEqual(response.status_int, 201)
        mock_urlfetch.fetch.assert_called_with(url=expected_url)

        data = json.loads(response.body)
        self.assertEqual(data, expected_count)

        # Check datastore
        datastore_data = ScoreModel.query(ScoreModel.week == expected_week).fetch(expected_count+1)
        self.assertEqual(len(datastore_data), expected_count)
        self.assertEqual(datastore_data[0].to_dict(), self._score_data_postseason()[0])
