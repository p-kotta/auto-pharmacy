import webapp2
from google.appengine.ext import ndb
from models.work import *
from templates import render


class WorksHandler(webapp2.RequestHandler):
    def get(self):

        self.response.write(render('head', {}))

        self.response.write(render('header', { 'current': 'works' }))

        for work in Work.query().order(+Work.priority).fetch():
            self.response.write(render('work', { 'work': work }))
            for photo in WorkPhoto.query(ancestor=ndb.Key(Work, work.key.id())).order(+WorkPhoto.priority).fetch():
                self.response.write(render('work-photo', { 'photo': photo }))

        self.response.write(render('footer', {}))