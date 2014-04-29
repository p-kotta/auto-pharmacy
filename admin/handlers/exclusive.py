import webapp2
from google.appengine.ext import ndb
from models.exclusive import *
from admin.templates import render

class ExclusiveAdminHandler(webapp2.RequestHandler):
    def get(self):

        self.response.write(render('exclusive', {'exclusive': Exclusive.query()}))

    def post(self):

        exclusive = Exclusive.query().fetch()
        if len(exclusive):
            exclusive = exclusive[0]
        else:
            exclusive = Exclusive()

        exclusive.text = self.request.get('text')
        exclusive.put()

        self.redirect('/exclusive/')