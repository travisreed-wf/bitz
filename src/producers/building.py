from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.resources import resource


class Building(polymodel.PolyModel):
    name = ndb.StringProperty(indexed=True)
    cost = ndb.LocalStructuredProperty(resource.Resource, indexed=False,
                                       repeated=True)
    production_per_ticket = ndb.LocalStructuredProperty(
        resource.Resource, indexed=False, repeated=True)
    ticks_per_day = ndb.IntegerProperty(indexed=True)
