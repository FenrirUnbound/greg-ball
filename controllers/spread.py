import json
from models.spread import Spread
import webapp2

class SpreadHandler(webapp2.RequestHandler):
    def get(self, year, week):
        year = int(year)
        week = int(week)

        spread = Spread()
        spread_data = spread.fetch(year=year, week=week)

        result = {
            'spread': spread_data
        }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps(result))

    def put(self, year, week):
        year = int(year)
        week = int(week)
        param = self.request.POST['spread']     # webapp2 treats POST body the same for PUT
        spread_data = json.loads(param)

        spread = Spread()
        result = spread.save(year=year, week=week, data=spread_data)

        self.response.set_status(201)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps({}))
