import json
from models.spread import Spread
import webapp2

class CommonSpreadHandler(webapp2.RequestHandler):
    def _send_response(self, data={}):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps(data))

class SpreadsHandler(CommonSpreadHandler):
    def get(self, year, week):
        year = int(year)
        week = int(week)

        spread = Spread()
        spread_data = spread.fetch(year=year, week=week)

        result = {
            'spread': spread_data
        }

        self._send_response(result)

    def put(self, year, week):
        """
        WARNING! Use of this endpoint will create odd side-effects
        This endpoint does not acknowledge the 'game_id' property of spread data
        """
        year = int(year)
        week = int(week)
        param = self.request.POST['spread']     # webapp2 treats POST body the same for PUT
        spread_data = json.loads(param)

        spread = Spread()
        result = spread.save(year=year, week=week, data=spread_data)

        self.response.set_status(201)
        self._send_response()

class SpreadHandler(CommonSpreadHandler):
    def get(self, year, week, game):
        year = int(year)
        week = int(week)
        game = int(game)

        spread = Spread()
        result = spread.fetch_by_id(year=year, week=week, game_id=game)

        self._send_response(result)

    def put(self, year, week, game):
        year = int(year)
        week = int(week)
        game = int(game)
        spread_data = json.loads(self.request.POST['spread'])

        spread = Spread()
        result = spread.save_by_id(year=year, week=week, game_id=game, data=spread_data)

        self._send_response()


