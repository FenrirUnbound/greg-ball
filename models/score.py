import json

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from models.datastore.score_ds import ScoreModel
from models.lib.score_formatter import ScoreFormatter

class Score(object):
    def __init__(self):
        self._remote = _ScoreSource()
        self.url_reg = 'http://www.nfl.com/liveupdate/scorestrip/scorestrip.json'

    def fetch(self, game_id=None, week=0, year=0):
        if game_id is not None:
            return self._fetch_game_by_id(game_id=game_id, week=week, year=year)
        else:
            game_data = self._remote.fetch()
            return game_data

    def save(self, data, game_id, week=0, year=0):
        key = self._generate_key(game_id=game_id, week=week, year=year)
        score_data = {'key': key}
        score_data.update(data)

        ScoreModel(**score_data).put()

        return 1

    def _fetch_game_by_id(self, game_id, week, year):
        key = self._generate_key(game_id=game_id, week=week, year=year)
        data = key.get()

        return data.to_dict()

    def _generate_key(self, game_id, week, year):
        return ndb.Key('year', year, 'week', week, ScoreModel, game_id)

class _ScoreSource(object):
    def __init__(self):
        self.url_reg = 'http://www.nfl.com/liveupdate/scorestrip/scorestrip.json'
        self.formatter = ScoreFormatter()

    def fetch(self):
        fetch_response = urlfetch.fetch(url=self.url_reg)
        response_content = self.formatter.format(fetch_response.content)
        game_data = json.loads(response_content)

        result = []
        for game in game_data:
            value = self._create_dict_from_data(data=game)
            result.append(value)

        return result

    def _create_dict_from_data(self, data):
        result = {
            'away_name': data[4],
            'away_score': int(data[5]),
            'game_id': int(data[10]),
            'home_name': data[6],
            'home_score': int(data[7]),
            'week': int(data[12][3:]),
            'year': int(data[13])
        }
        return result
