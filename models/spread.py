from google.appengine.ext import ndb

from models.datastore.spread_ds import SpreadModel

class Spread(object):
    def __init__(self, year=1990):
        self._datastore = SpreadModel()
        self._year = year

    def fetch(self, year=None, week=0):
        # For backwards compatability
        year = year or self._year

        result = []
        data = self._datastore.fetch_spread(year=year, week=week, count=20)

        for game in data:
            result.append(game.to_dict())

        return result

    def save(self, year=None, week=0, data=[]):
        # For backwards compatability
        year = year or self._year

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