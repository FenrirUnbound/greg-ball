from google.appengine.ext import ndb

class ScoreModel(ndb.Model):
    """ Datastore model for Spread data

    away_name:      away team's name
    away_score:     away team's score
    game_clock:     the amount of time remaining in the game
    game_day:       the day of the week that the game is played on
    game_id:        unique identifier of the game
    game_status:    playing status of the game (final, pregame, currently playing, etc)
    game_time:      the time that the game starts at
    home_name:      home team's name
    home_score:     home team's score
    week:           game week
    year:           season
    """
    away_name = ndb.StringProperty(default='')  # TODO require
    away_score = ndb.IntegerProperty(required=True)
    game_clock = ndb.StringProperty(default='00:00')
    game_day = ndb.StringProperty(default='')
    game_id = ndb.IntegerProperty(required=True)
    game_status = ndb.StringProperty(default='')
    game_time = ndb.StringProperty(default='00:00')
    home_name = ndb.StringProperty(default='')  # TODO require
    home_score = ndb.IntegerProperty(required=True)
    week = ndb.IntegerProperty(required=True)
    year = ndb.IntegerProperty(required=True)
