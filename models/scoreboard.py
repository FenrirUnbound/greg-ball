import json

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from models.datastore.score_ds import ScoreModel
from models.helper.score_formatter import ScoreFormatter

class Scoreboard(object):
    WEEK_POSTSEASON = 18

    def __init__(self):
        self._remote_postseason = _SourcePostseason()

    def fetch(self, year, week):
        game_data = []

        if week < self.WEEK_POSTSEASON:
            pass
        else:
            game_data = self._remote_postseason.fetch(week)

        return self._save(year=year, week=week, data=game_data)

    def _save(self, year, week, data):
        parent_key = self._generate_parent_key(year=year, week=week)
        exist = self._find_existing_entries(key=parent_key, data=data)

        to_save = []
        for score_data in data:
            game_id = score_data['game_id']
            if game_id in exist:
                # update game
                game = self._update_model(exist[game_id], score_data)
                to_save.append(game)
            else:
                # unsaved game
                game = {'parent': parent_key}
                game.update(score_data)
                score = ScoreModel(**game)

                to_save.append(score)
        result = ndb.put_multi(entities=to_save)
        return len(to_save)

    def _find_existing_entries(self, key, data):
        result = {}

        game_ids = []
        for game in data:
            game_ids.append(game['game_id'])

        query = ScoreModel.query(ScoreModel.game_id.IN(game_ids), ancestor=key)
        score_data = query.fetch(len(data))

        for game in score_data:
            result[game.game_id] = game

        return result

    def _generate_parent_key(self, year, week):
        return ndb.Key('year', year, 'week', week)

    def _update_model(self, model, data):
        for prop in model._properties:
            setattr(model, prop, data[prop])
        return model


class _SourceScoreboard(object):
    def __init__(self):
        self.formatter = ScoreFormatter()

    def fetch(self, week):
        raise NotImplementedError("Subclasses should implement this")

class _SourcePostseason(_SourceScoreboard):
    def __init__(self):
        self.url = 'http://www.nfl.com/liveupdate/scorestrip/postseason/scorestrip.json'
        super(_SourcePostseason, self).__init__()

    def fetch(self, week):
        response = urlfetch.fetch(url=self.url)
        content = self.formatter.format(response.content)
        game_data = content

        result = []
        for game in game_data:
            value = self._create_dict_from_data(data=game)
            result.append(value)
        return result

    def _create_dict_from_data(self, data):
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
