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
