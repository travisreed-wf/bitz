from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Producer(polymodel.PolyModel):
    name = ndb.StringProperty()
    count = ndb.IntegerProperty()
    daily_cost = ndb.JsonProperty(indexed=False)
    production = ndb.JsonProperty(indexed=False)
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
