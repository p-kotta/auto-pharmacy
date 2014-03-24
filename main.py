#!/usr/bin/env python

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

WORK_TEMPLATE = """\
    <h2 id="%s">%s</h2>
    <p>%s</p>
"""
class WorksHandler(webapp2.RequestHandler):
    def get(self):
        for work in Work.query().order(+Work.priority).fetch():
            self.response.write(WORK_TEMPLATE % (work.name, work.title, work.description))

class AdminHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.write('Hello, ' + user.nickname())

WORK_ADMIN_TEMPLATE = """\
    <form action="" method="post">
        <input name="key" type="hidden" value="%s"/>
        <input name="name" value="%s"/>
        <input name="title" value="%s"/>
        <textarea name="description">%s</textarea>
        <input name="priority" value="%s"/>
        <input type="submit" value="Submit"/>
    </form>
"""
class WorksAdminHandler(webapp2.RequestHandler):
    def get(self):
        # edit existing
        for work in Work.query().order(+Work.priority).fetch():
            self.response.write(WORK_ADMIN_TEMPLATE % (work.key.urlsafe(), work.name, work.title, work.description, work.priority))

        # add new
        self.response.write(WORK_ADMIN_TEMPLATE % ('', '', '', '', ''))

    def post(self):
        # try get existing...
        work = None
        try:
            work = ndb.Key(urlsafe=self.request.get('key')).get()
        except TypeError:
            pass
        # or create new one
        if not work:
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
