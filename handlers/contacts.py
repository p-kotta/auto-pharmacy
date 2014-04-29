import webapp2
from google.appengine.ext import ndb
from models.work import *
from templates import render


class ContactsHandler(webapp2.RequestHandler):
    def get(self):

        self.response.write(render('head', {}))
        self.response.write(render('header', { 'current': 'contacts' }))
        self.response.write(render('contacts', {}))
        self.response.write(render('footer', {}))