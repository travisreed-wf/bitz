from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Worker(polymodel.PolyModel):
    name = ndb.StringProperty()
    count = ndb.IntegerProperty(indexed=False)
    daily_cost = ndb.LocalStructuredProperty(kind="Resource", repeated=True)
    production = ndb.LocalStructuredProperty(kind="Resource", repeated=True)
    production_rate = ndb.IntegerProperty(indexed=True)


class Player(Worker):
    pass

