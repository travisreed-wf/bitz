from copy import copy
import math

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.resources import resource


class Action(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    icon_class = ndb.StringProperty(indexed=False)
    button_class = ndb.StringProperty(indexed=False)

    @staticmethod
    def get_gather_wood_action():
        return Action(
            name="gather_wood", icon_class="glyphicon glyphicon-tree-deciduous",
            button_class="btn btn-primary")

    @staticmethod
    def get_gather_food_action():
        return Action(
            name="gather_food", icon_class="glyphicon glyphicon-apple",
            button_class="btn btn-success")

    @staticmethod
    def get_hunt_action():
        return Action(
            name="hunt", icon_class="glyphicon glyphicon-tree-conifer",
            button_class="btn btn-danger"
        )

    @staticmethod
    def get_gather_water_action():
        return Action(
            name="gather_water", icon_class="glyphicon glyphicon glyphicon-tint",
            button_class="btn btn-info"
        )



class Tile(polymodel.PolyModel):
    name = ndb.StringProperty(indexed=False)
    type = ndb.StringProperty(indexed=False)
    production = ndb.LocalStructuredProperty(
        resource.Resource, repeated=True, indexed=False)
    resources_available = ndb.LocalStructuredProperty(
        resource.Resource, repeated=True, indexed=False)
    actions = ndb.LocalStructuredProperty(Action, repeated=True, indexed=False)

    def get_resource_production(self, resource_name):
        for resource in self.production:
            if resource.name == resource_name:
                return resource

    def get_resource_available(self, resource_name):
        for resource in self.resources_available:
            if resource.name == resource_name:
                return resource

    def consume_resource(self, resource):
        resource_available = self.get_resource_available(resource.name)
        if not resource_available:
            raise AttributeError

        resource_available.count -= resource.count
        if resource_available.count < 0:
            raise AttributeError
        self.put()


class Trees(Tile):

    def gather_wood(self, worker_resources):
        produced_wood = copy(self.get_resource_production("Wood"))

        worker_health = None
        worker_wood = None
        worker_axe = None
        consumed_resources = []
        produced_resources = [produced_wood]
        for worker_resource in worker_resources:
            if worker_resource.name == "Axe" and worker_resource.count > 1:
                worker_axe = worker_resource
            elif worker_resource.name == "Health":
                worker_health = worker_resource
            elif worker_resource.name == "Wood":
                worker_wood = worker_resource

        if worker_axe:
            worker_axe.count -= 1
            consumed_axe = copy(worker_axe)
            consumed_axe.count = 1
            consumed_resources.append(consumed_axe)
            produced_wood.count = produced_wood.count * 3
        else:
            consumed_health = copy(worker_health)
            consumed_health.count = 1
            consumed_resources.append(consumed_health)
            worker_health.count -= 1
        worker_wood.count += produced_wood.count

        for produced_resource in produced_resources:
            self.consume_resource(produced_resource)
        return produced_resources, consumed_resources


    @staticmethod
    def get_trees_dense():
        gather_wood = Action.get_gather_wood_action()
        gather_food = Action.get_gather_food_action()
        hunt = Action.get_hunt_action()
        actions = [gather_wood, gather_food, hunt]
        wood = resource.Wood(count=1)
        wood2 = resource.Wood(count=100000)
        return Trees(name="Dense Trees", type="Base", production=[wood],
                     resources_available=[wood2], actions=actions)

    @staticmethod
    def get_trees():
        gather_wood = Action.get_gather_wood_action()
        gather_food = Action.get_gather_food_action()
        hunt = Action.get_hunt_action()
        actions = [gather_wood, gather_food, hunt]
        wood = resource.Wood(count=1)
        wood2 = resource.Wood(count=10000)
        return Trees(name="Trees", type="Base", production=[wood],
                     resources_available=[wood2], actions=actions)

    @staticmethod
    def get_trees_sparse():
        gather_wood = Action.get_gather_wood_action()
        gather_food = Action.get_gather_food_action()
        hunt = Action.get_hunt_action()
        actions = [gather_wood, gather_food, hunt]
        wood = resource.Wood(count=1)
        wood2 = resource.Wood(count=1000)
        return Trees(name="Sparse Trees", type="Base", production=[wood],
                     resources_available=[wood2], actions=actions)

class Plains(Tile):

    @staticmethod
    def get_plains():
        return Plains(name="Plains", type="Base", production=[])


class River(Tile):

    @staticmethod
    def get_river():
        gather_water = Action.get_gather_water_action()
        actions = [gather_water]
        water = resource.Water(count=1)
        water2 = resource.Water(count=100000000000000000000)
        return River(name="River", type="Base", production=[water],
                     resources_available=[water2], actions=actions)


class Location(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    type = ndb.StringProperty(indexed=True)
    tiles = ndb.KeyProperty(kind=Tile, repeated=True)
    tiles_per_row = ndb.ComputedProperty(
        lambda self: round(math.sqrt(len(self.tiles))))
