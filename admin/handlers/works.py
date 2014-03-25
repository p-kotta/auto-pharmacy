import webapp2
from google.appengine.ext import ndb
from models.work import *
from admin.templates import render

class WorksAdminHandler(webapp2.RequestHandler):
    def get(self):
        works = []
        for work in Work.query().order(+Work.priority).fetch():
            photos = []
            works.append({
                'key': work.key.urlsafe(),
                'id': work.key.id(),
                'name': work.name,
                'title': work.title,
                'description': work.description,
                'priority': work.priority,
                'photos': photos
            })
            for photo in WorkPhoto.query(ancestor=ndb.Key(Work, work.key.id())).order(+WorkPhoto.priority).fetch():
                photos.append({
                    'work': work.key.urlsafe(),
                    'key': photo.key.urlsafe(),
                    'id': photo.key.id(),
                    'title': photo.title,
                    'url': photo.url,
                    'priority': photo.priority
                })
        self.response.write(render('works', { 'works': works }))

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
                photo.priority = int(self.request.get('priority'))
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
