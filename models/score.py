from google.appengine.ext import ndb

class Score(object):
    def __init__(self):
        pass

    def fetch(self, game_id, week=0, year=0):
        key = ndb.Key('year', year, 'week', week, 'ScoreModel', game_id)
        data = key.get()

        return data.to_dict()
