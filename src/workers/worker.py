from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Worker(polymodel.PolyModel):
    name = ndb.StringProperty()
    count = ndb.IntegerProperty(indexed=False)
    daily_cost = ndb.LocalStructuredProperty(kind="Resource", repeated=True,
                                             indexed=False)
    production = ndb.LocalStructuredProperty(kind="Resource", repeated=True,
                                             indexed=False)
    production_rate = ndb.IntegerProperty(indexed=False)
    resources = ndb.LocalStructuredProperty(kind="Resource", repeated=True,
                                            indexed=False)


class Player(Worker):
    pass

