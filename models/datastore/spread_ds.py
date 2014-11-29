from google.appengine.ext import ndb

class SpreadModel(ndb.Model):
    """ Datastore model for Spread data

    week:       game week
    year:       season
    game_line:  the game line
                non-negative floating-point number.
    game_odds:  the game spread
                signed floating-point number. Negative numbers ALWAYS infer
                Home team is favorited; positive numbers ALWAYS infer Away
                team is favorite
    """
    game_id = ndb.IntegerProperty(required=True)
    week = ndb.IntegerProperty(required=True)
    year = ndb.IntegerProperty(required=True)
    game_line = ndb.FloatProperty(indexed=False)
    game_odds = ndb.FloatProperty(indexed=False)

    def fetch_spread(self, year, week, count=20):
        ancestor_key = self._generate_key(year=year, week=week)
        query = self.query(ancestor=ancestor_key).order(SpreadModel.game_id)

        return query.fetch(count)

    @classmethod
    def save_spread(cls, year, week, data=[]):
        ancestor_key = cls.generate_key(year=year, week=week)

        spread_data = []
        for item in data:
            game = item.to_dict()
            game.update({'parent': ancestor_key})

            spread_data.append(SpreadModel(**game))

        result = ndb.put_multi(spread_data)

        return len(spread_data)


    def _generate_key(self, year, week):
        return ndb.Key('year', year, 'week', week)

    @classmethod
    def generate_key(cls, year, week):
        return ndb.Key('year', year, 'week', week)