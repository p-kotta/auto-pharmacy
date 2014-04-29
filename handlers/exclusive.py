import webapp2
from google.appengine.ext import ndb
from models.exclusive import *
from templates import render


class ExclusiveHandler(webapp2.RequestHandler):
    def get(self):

        if len(Exclusive.query().fetch()):
            entity = Exclusive.query().fetch(1)[0]
        else:
            entity = {'text': ''}

        self.response.write(render('exclusive', {'exclusive': entity}))