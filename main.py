from controllers import score, status, spread
import webapp2
from webapp2_extras import routes

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

application = webapp2.WSGIApplication([
    routes.PathPrefixRoute('/api/v1', [
        webapp2.Route('/status', status.Status),
        webapp2.Route('/spread/year/<year:\d+>/week/<week:\d+>', spread.SpreadsHandler),
        webapp2.Route('/spread/year/<year:\d+>/week/<week:\d+>/game/<game:\d+>', spread.SpreadHandler),
        webapp2.Route('/score/year/<year:\d+>/week/<week:\d+>', score.ScoresHandler),
        webapp2.Route('/score/year/<year:\d+>/week/<week:\d+>/game/<game:\d+>', score.ScoreHandler)
    ])
], debug=True)
