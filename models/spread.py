from models.datastore.spread_ds import SpreadModel

class Spread(object):
    def __init__(self, year=1990, week=99):
        self._datastore = SpreadModel()
        self._year = year

    def fetch(self, week=0):
        result = []
        data = self._datastore.fetch_spread(year=self._year, week=week, count=20)

        for game in data:
            result.append(game.to_dict())

        return result