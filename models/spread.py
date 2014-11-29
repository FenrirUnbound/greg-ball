from google.appengine.ext import ndb

from models.datastore.spread_ds import SpreadModel

class Spread(object):
    def __init__(self):
        pass

    def fetch(self, year=1990, week=0, max_count=25):
        ancestor_key = self._generate_key(year=year, week=week)
        query = SpreadModel.query(ancestor=ancestor_key).order(SpreadModel.game_id)
        data = query.fetch(max_count)

        result = []
        for game in data:
            result.append(game.to_dict())

        return result

    def save(self, year=1990, week=0, data=[]):
        parent_key = self._generate_key(year=year, week=week)

        to_save = []
        for spread_data in data:
            game = {'parent': parent_key}
            game.update(spread_data)
            spread = SpreadModel(**game)
            to_save.append(spread)

        result = ndb.put_multi(entities=to_save)
        # print result
        return len(to_save)

    def _generate_key(self, year, week):
        return ndb.Key('year', year, 'week', week)