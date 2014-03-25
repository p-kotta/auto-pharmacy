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

WORK_PHOTO_TEMPLATE = """\
    <img src="%s" alt=""/>
    <span>%s</span>
"""

class WorksHandler(webapp2.RequestHandler):
    def get(self):
        for work in Work.query().order(+Work.priority).fetch():
            self.response.write(WORK_TEMPLATE % (work.name, work.title, work.description))
            for photo in WorkPhoto.query(ancestor=ndb.Key(Work, work.key.id())).order(+WorkPhoto.priority).fetch():
                self.response.write(WORK_PHOTO_TEMPLATE % (photo.url, photo.title))


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
        <input type="submit" name="delete" value="Delete!"/>
    </form>
"""

WORK_PHOTO_ADMIN_TEMPLATE = """\
    <form action="" method="post">
        <input name="work" type="hidden" value="%s"/>
        <input name="key" type="hidden" value="%s"/>
        <input name="title" value="%s"/>
        <input name="url" value="%s"/>
        <input type="submit" value="Submit"/>
        <input type="submit" name="delete" value="Delete!"/>
    </form>
"""

class WorksAdminHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('<h1>Works</h1>')
        # edit existing
        for work in Work.query().order(+Work.priority).fetch():
            self.response.write('<h2>Work "%s"</h2>' % work.name)
            self.response.write(WORK_ADMIN_TEMPLATE % (work.key.urlsafe(), work.name, work.title, work.description, work.priority))
            self.response.write('<h3>Photos</h3>')
            for photo in WorkPhoto.query(ancestor=ndb.Key(Work, work.key.id())).order(+WorkPhoto.priority).fetch():
                self.response.write(WORK_PHOTO_ADMIN_TEMPLATE % (work.key.urlsafe(), photo.key.urlsafe(), photo.title, photo.url))
            self.response.write(WORK_PHOTO_ADMIN_TEMPLATE % (work.key.urlsafe(), '', 'Title', 'URL'))

        # add new
        self.response.write(WORK_ADMIN_TEMPLATE % ('', 'name', 'Title', 'Description', '42'))

    def post(self):
        # delete work or photo
        if self.request.get('delete'):
            ndb.Key(urlsafe=self.request.get('key')).delete()

        else:
            # post about work photo
            if self.request.get('work'):
                # try get existing...
                photo = None
                try:
                    photo = ndb.Key(urlsafe=self.request.get('key')).get()
                except TypeError:
                    pass
                # or create new one
                if not photo:
                    work = ndb.Key(urlsafe=self.request.get('work')).get()
                    photo = WorkPhoto(parent=ndb.Key(Work, work.key.id()))

                photo.title = self.request.get('title')
                photo.url = self.request.get('url')
                photo.put()

            # post about work
            else:
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

class WorkPhoto(ndb.Model):
    priority = ndb.IntegerProperty()
    title = ndb.StringProperty()
    url = ndb.StringProperty()
