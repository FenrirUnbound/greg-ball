import json
from models.spread import Spread
import webapp2

class SpreadHandler(webapp2.RequestHandler):
    def get(self, year, week):
        year = int(year)
        week = int(week)
        spread = Spread(year=year)
        spread_data = spread.fetch(week=week)

        result = {
            'spread': spread_data
        }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps(result))

    def post(self, year, week):
        year = int(year)
        week = int(week)
        param = self.request.POST['spread']
        spread_data = json.loads(param)

        spread = Spread(year=year)
        result = spread.save(week=week, data=spread_data)

        self.response.set_status(201)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps({}))
