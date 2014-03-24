#!/usr/bin/env python

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class WorksHandler(webapp2.RequestHandler):
    def get(self):
        for work in Work.query().order(+Work.priority).fetch():
            self.response.write('<h2 id="%s">%s</h2>' % (work.name, work.title))
            self.response.write('<p>%s</p>' % work.description)

class AdminHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.write('Hello, ' + user.nickname())

WORKS_ADMIN_TEMPLATE = """\
    <form action="" method="post">
        <input name="priority" value="42"/>
        <input name="name" value="name"/>
        <input name="title" value="Title"/>
        <textarea name="description">Description</textarea>
        <input type="submit" value="Submit"/>
    </form>
"""
class WorksAdminHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(WORKS_ADMIN_TEMPLATE)

    def post(self):
        work = Work()
        work.priority = int(self.request.get('priority'))
        work.name = self.request.get('name')
        work.title = self.request.get('title')
        work.description = self.request.get('description')
        work.put()
        self.redirect('/works/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/works/', WorksHandler),

    ('/admin/', AdminHandler),
    ('/admin/works/', WorksAdminHandler)
], debug=True)


class Work(ndb.Model):
    priority = ndb.IntegerProperty()
    name = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.StringProperty()
