from datetime import datetime
import json
import webapp2

from libraries.schedule import Schedule
from models.scoreboard import Scoreboard

class CronScoreHandler(webapp2.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.schedule = Schedule()
        self.scoreboard = Scoreboard()
        super(CronScoreHandler, self).__init__(*args, **kwargs)

    def get(self):
        current_week = self.schedule.week()
        current_season = self.schedule.season_year()
        result = self.scoreboard.fetch(year=current_season, week=current_week)

        self.response.status_code = 201
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps(result))
