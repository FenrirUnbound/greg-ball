from google.appengine.ext import ndb

class Spread(ndb.Model):
    game_id = ndb.IntegerProperty()
    game_line = ndb.FloatProperty(indexed=False)
    game_odds = ndb.FloatProperty(indexed=False)
