import json
import webapp2

from models.score import Score

class ScoreHandler(webapp2.RequestHandler):
    def get(self, year, week, game):
        year = int(year)
        week = int(week)
        game = int(game)

        score = Score()
        result = score.fetch(game_id=game, week=week, year=year)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps(result))
