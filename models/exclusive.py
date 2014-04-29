from google.appengine.ext import ndb

class Exclusive(ndb.Model):
    text = ndb.TextProperty()