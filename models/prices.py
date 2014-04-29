from google.appengine.ext import ndb

class Prices(ndb.Model):
    name = ndb.StringProperty()

class PricesRow(ndb.Model):
    parentId = ndb.IntegerProperty()
    name = ndb.StringProperty()
    cost = ndb.IntegerProperty()

