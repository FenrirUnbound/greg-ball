import json
import webapp2

from models.score import Score

class CommonScoreHandler(webapp2.RequestHandler):
    def __init__(self, *args, **kwargs):
        self._score = Score()
        super(CommonScoreHandler, self).__init__(*args, **kwargs)

    def _send_response(self, result={}):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps(result))

class ScoreHandler(CommonScoreHandler):
    def get(self, year, week, game):
        year = int(year)
        week = int(week)
        game = int(game)

        result = self._score.fetch(game_id=game, week=week, year=year)

        self._send_response(result=result)

    def put(self, year, week, game):
        year = int(year)
        week = int(week)
        game = int(game)
        # TODO error handling
        data = json.loads(self.request.POST['game'])

        result = self._score.save(data=data, game_id=game, week=week, year=year)

        self._send_response()

class ScoresHandler(CommonScoreHandler):
    def get(self, year, week):
        year = int(year)
        week = int(week)

        result = self._score.fetch(week=week, year=year)

        self._send_response(result)
