import json

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from models.datastore.score_ds import ScoreModel
from models.helper.score_formatter import ScoreFormatter

class Score(object):
    def __init__(self):
        self._remote = _ScoreSource()
        self.url_reg = 'http://www.nfl.com/liveupdate/scorestrip/scorestrip.json'

    def fetch(self, year, week, game_id=None):
        if game_id is not None:
            return self._fetch_game_by_id(game_id=game_id, week=week, year=year)
        else:
            # TODO fetch from source iff current data is stale
            game_data = self._remote.fetch(week)
            # TODO Save data upon fetching remote
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
    REG_SEASON = 17

    def __init__(self):
        self.url_reg = 'http://www.nfl.com/liveupdate/scorestrip/scorestrip.json'
        self.url_post = 'http://www.nfl.com/liveupdate/scorestrip/postseason/scorestrip.json'
        self.formatter = ScoreFormatter()

    def fetch(self, week):
        url = ''

        if week <= self.REG_SEASON:
            url = self.url_reg
        else:
            url = self.url_post

        fetch_response = urlfetch.fetch(url=url)
        content = self.formatter.format(fetch_response.content)
        game_data = content

        result = []
        for game in game_data:
            if week <= self.REG_SEASON:
                value = self._create_dict_from_data(data=game)
                result.append(value)
            else:
                value = self._create_dict_from_post_data(data=game)
                result.append(value)

        return result

    def _create_dict_from_data(self, data):
        result = {
            'away_name': data[4],
            'away_score': int(data[5]) if data[5] is not None else 0,
            'game_clock': data[3] if data[3] is not None else '00:00',
            'game_day': data[0],
            'game_id': int(data[10]),
            'game_status': data[2],
            'game_time': data[1],
            'home_name': data[6],
            'home_score': int(data[7]) if data[7] is not None else 0,
            'week': int(data[12][3:]),
            'year': int(data[13])
        }
        return result

    def _create_dict_from_post_data(self, data):
        result = {
            'away_name': data[5],
            'away_score': int(data[6]) if data[6] is not None else 0,
            'game_clock': data[3] if data[3] is not None else '00:00',
            'game_day': data[0],
            'game_id': int(data[12]),
            'game_status': data[2],
            'game_time': data[1],
            'home_name': data[8],
            'home_score': int(data[9]) if data[9] is not None else 0,
            'week': int(data[15][4:]),
            'year': int(data[16])
        }
        return result
