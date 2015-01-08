import json

from google.appengine.ext import ndb

from models.datastore.score_ds import ScoreModel

class Score(object):
    MAX_GAMES = 16

    def __init__(self):
        self.formatter = _InvalidGameFormatter(nextFormatter=_DictFormatter())

    def fetch(self, year, week, game_id=None):
        if game_id is not None:
            return self._fetch_game_by_id(game_id=game_id, week=week, year=year)
        else:
            return self._fetch_games_by_week(year=year, week=week)

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

    def _fetch_games_by_week(self, year, week):
        parent_key = self._generate_key(year=year, week=week)

        query = ScoreModel.query(ancestor=parent_key).order(ScoreModel.game_id)
        data = query.fetch(self.MAX_GAMES)

        return self.formatter.format(data=data)

    def _generate_key(self, week, year, game_id=None):
        if game_id is None:
            return ndb.Key('year', year, 'week', week)
        else:
            return ndb.Key('year', year, 'week', week, ScoreModel, game_id)

    def _to_dict(self, score_models_data):
        result = []

        for game in score_models_data:
            result.append(game.to_dict())

        return result

class _Formatter(object):
    def __init__(self, nextFormatter=None):
        self.next = nextFormatter

    def format(self, data):
        result = self._execute_format(data=data)
        if self.next != None:
            return self.next.format(result)
        return result

    def _execute_format(self, data):
        raise NotImplementedError

class _DictFormatter(_Formatter):
    def __init__(self, nextFormatter=None):
        super(_DictFormatter, self).__init__(nextFormatter=nextFormatter)

    def _execute_format(self, data):
        result = []
        for game in data:
            result.append(game.to_dict())
        return result

class _InvalidGameFormatter(_Formatter):
    def __init__(self, nextFormatter=None):
        super(_InvalidGameFormatter, self).__init__(nextFormatter=nextFormatter)

    def _execute_format(self, data):
        result = []
        for game in data:
            if hasattr(game, 'game_id'):
                if game.game_id > 0:
                    result.append(game)
            elif game['game_id'] > 0:
                result.append(game)

        return result
