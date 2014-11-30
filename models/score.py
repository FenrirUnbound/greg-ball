from google.appengine.ext import ndb

from models.datastore.score_ds import ScoreModel

class Score(object):
    def __init__(self):
        pass

    def fetch(self, game_id, week=0, year=0):
        key = ndb.Key('year', year, 'week', week, 'ScoreModel', game_id)
        data = key.get()

        return data.to_dict()

    def save(self, data, game_id, week=0, year=0):
        key = ndb.Key('year', year, 'week', week, 'ScoreModel', game_id)
        score_data = {'key': key}
        score_data.update(data)

        ScoreModel(**score_data).put()

        return 1
