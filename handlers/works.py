import webapp2
from google.appengine.ext import ndb
from models.work import *
from templates import render


class WorksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(render(
            'works',
            { 'works': Work.get_root()['children'] }))

