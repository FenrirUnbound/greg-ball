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

    def fetch_by_id(self, year=1990, week=0, game_id=0):
        ancestor_key = self._generate_key(year=year, week=week)
        query = SpreadModel.query(SpreadModel.game_id == game_id, ancestor=ancestor_key)
        data = query.fetch(1)

        return data[0].to_dict()

    def save(self, year=1990, week=0, data=[]):
        parent_key = self._generate_key(year=year, week=week)
        exist = self._find_existing_entries(key=parent_key, data=data)

        to_save = []
        for spread_data in data:
            game_id = spread_data['game_id']
            if game_id in exist:
                game = self._update_model(exist[game_id], spread_data)
                to_save.append(game)
            else:
                game = {'parent': parent_key}
                game.update(spread_data)
                spread = SpreadModel(**game)

                to_save.append(spread)

        result = ndb.put_multi(entities=to_save)
        return len(to_save)

    def save_by_id(self, year=1990, week=0, game_id=0, data={}):
        key = self._generate_key(year=year, week=week, game_id=game_id)
        game = key.get()
        if game is None:
            spread_data = {'key': key}
            spread_data.update(data)

            SpreadModel(**spread_data).put()
        else:
            for prop in data:
                setattr(game, prop, data[prop])
            game.put()

        return 1

    def _find_existing_entries(self, key, data):
        result = {}

        game_ids = []
        for game in data:
            game_ids.append(game['game_id'])

        query = SpreadModel.query(SpreadModel.game_id.IN(game_ids), ancestor=key)
        spread_data = query.fetch(len(data))

        for game in spread_data:
            result[game.game_id] = game

        return result

    def _update_model(self, model, data):
        for prop in model._properties:
            setattr(model, prop, data[prop])
        return model

    def _generate_key(self, year, week, game_id=0):
        if game_id > 0:
            return ndb.Key('year', year, 'week', week, 'SpreadModel', game_id)
        else:
            return ndb.Key('year', year, 'week', week)
