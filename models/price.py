from google.appengine.ext import ndb

class Price(ndb.Model):
    name = ndb.StringProperty()

class PriceRow(ndb.Model):
    parentId = ndb.IntegerProperty()
    name = ndb.StringProperty()
    cost = ndb.IntegerProperty()

