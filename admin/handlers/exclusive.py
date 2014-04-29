import webapp2
from google.appengine.ext import ndb
from models.exclusive import *
from admin.templates import render

class ExclusiveAdminHandler(webapp2.RequestHandler):
    def get(self):

        exclusive = Exclusive.query().fetch()
        if len(exclusive):
            exclusive = exclusive[0]
        else:
            exclusive = {'text': ''}

        self.response.write(render('exclusive', {'exclusive': exclusive}))

    def post(self):

        exclusive = Exclusive.query().fetch()
        if len(exclusive):
            exclusive = exclusive[0]
        else:
            exclusive = Exclusive()

        exclusive.text = self.request.get('text')
        exclusive.put()

        self.redirect('/exclusive/')