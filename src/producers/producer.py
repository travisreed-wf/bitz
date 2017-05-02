from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.locations.action import Action
from src.resources import resource


class Producer(polymodel.PolyModel):
    name = ndb.StringProperty(indexed=True)
    daily_trigger_count = ndb.IntegerProperty(indexed=True)
    actions = ndb.LocalStructuredProperty(Action, repeated=True, indexed=False)
    tile = ndb.KeyProperty(kind="Tile", indexed=False)
    worker_info = ndb.JsonProperty()
    cost = ndb.LocalStructuredProperty(resource.Resource, indexed=False,
                                       repeated=True)

    def build_lumberyard(self, tile, builder):
        wood = resource.Wood.create(count=10000)
        builder.remove_resource(wood)
        action = Action.get_gather_wood_action()
        worker_info = {
            'gather_wood': [builder.key]
        }
        producer = Producer(
            name="Lumberyard", cost=wood, worker_info=worker_info, tile=tile.key,
            actions=[action], daily_trigger_count=1440)
        producer.put()

    def trigger(self):
        for action in self.actions:
            name = action.name
            workers = self.worker_info.get(name)
            for worker_key in workers:
                worker = worker.get()
                action.perform(self.tile.get(), worker, clicks=worker.count)

    def upgrade(self, upgraded_name):
        pass


class BaseProducer(Producer):
    def cost(self, current_count, to_add=1):
        raise NotImplementedError("Subclass must implement abstract method")


class DailyProducer(Producer):
    def cost(self, current_count, to_add=1):
        raise NotImplementedError("Subclass must implement abstract method")


class Lumberyard(BaseProducer):
    def cost(self, current_count, to_add=1):
        pass
