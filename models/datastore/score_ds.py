from google.appengine.ext import ndb

class ScoreModel(ndb.Model):
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
    away_score = ndb.IntegerProperty(required=True)
    game_id = ndb.IntegerProperty(required=True)
    home_score = ndb.IntegerProperty(required=True)
    week = ndb.IntegerProperty(required=True)
    year = ndb.IntegerProperty(required=True)
