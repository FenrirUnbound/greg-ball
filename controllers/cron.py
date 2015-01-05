import json
import webapp2

from models.scoreboard import Scoreboard

class CronScoreHandler(webapp2.RequestHandler):
    def post(self):
        scoreboard = Scoreboard()
        result = scoreboard.fetch(year=2014, week=18)

        self.response.status_code = 201
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps(result))
