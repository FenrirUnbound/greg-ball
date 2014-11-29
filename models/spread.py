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

    def _generate_key(self, year, week):
        return ndb.Key('year', year, 'week', week)
