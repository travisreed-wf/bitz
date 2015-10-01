from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

class Producer(polymodel.PolyModel):
    name = ndb.StringProperty()
    count = ndb.IntegerProperty(indexed=False)
    daily_cost = ndb.LocalStructuredProperty(kind="Resource", repeated=True)
    production = ndb.LocalStructuredProperty(kind="Resource", repeated=True)
    production_rate = ndb.IntegerProperty(indexed=True)

    def cost(self, current_count, to_add=1):
        raise NotImplementedError("Subclass must implement abstract method")

class BaseProducer(Producer):
    def cost(self, current_count, to_add=1):
        raise NotImplementedError("Subclass must implement abstract method")

class DailyProducer(Producer):
    def cost(self, current_count, to_add=1):
        raise NotImplementedError("Subclass must implement abstract method")

class Lumberyard(BaseProducer):
    def cost(self, current_count, to_add=1):
        pass
