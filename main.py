#!/usr/bin/env python

import webapp2
from google.appengine.api import users
from handlers.works import *
from handlers.prices import *
from handlers.contacts import *
from handlers.exclusive import *
from admin.handlers.works import *
from admin.handlers.exclusive import *


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class AdminHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.write('Hello, ' + user.nickname())


app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/works/', WorksHandler),
    ('/prices/', PricesHandler),
    ('/contacts/', ContactsHandler),
    ('/exclusive/', ExclusiveHandler),

    ('/admin/', AdminHandler),
    ('/admin/works/', WorksAdminHandler),
    ('/admin/exclusive/', ExclusiveAdminHandler)
], debug=True)
