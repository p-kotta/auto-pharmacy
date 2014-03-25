from google.appengine.ext import ndb

class Work(ndb.Model):
    priority = ndb.IntegerProperty()
    name = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.StringProperty()

class WorkPhoto(ndb.Model):
    priority = ndb.IntegerProperty()
    title = ndb.StringProperty()
    url = ndb.StringProperty()
