import webapp2
from google.appengine.ext import ndb
from models.work import *

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
