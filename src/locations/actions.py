from copy import copy

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Action(ndb):
    name = ndb.StringProperty(indexed=False)
    icon_class = ndb.StringProperty(indexed=False)
    button_class = ndb.StringProperty(indexed=False)

class GatherWood(Action):

    @staticmethod
    def create():
        action = Action(
            name="gather_wood", icon_class="glyphicon glyphicon-tree-deciduous",
            button_class="btn btn-primary")
        action.put()
        return action


    def perform(tile, worker_resources, clicks):
        produced_wood = copy(tile.get_resource_production("Wood"))

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
            worker_axe.count -= 1 * clicks
            consumed_axe = copy(worker_axe)
            consumed_axe.count = 1 * clicks
            consumed_resources.append(consumed_axe)
            produced_wood.count = produced_wood.count * 3 * clicks
        else:
            consumed_health = copy(worker_health)
            consumed_health.count = 1 * clicks
            consumed_resources.append(consumed_health)
            worker_health.count -= 1 * clicks
        worker_wood.count += produced_wood.count

        for produced_resource in produced_resources:
            tile.consume_resource(produced_resource)
        return produced_resources, consumed_resources


class GatherFood(Action):

    @staticmethod
    def create():
        action = Action(
            name="gather_food", icon_class="glyphicon glyphicon-apple",
            button_class="btn btn-success")
        action.put()
        return action


class GatherWater(Action):

    @staticmethod
    def create():
        action = Action(
            name="gather_water", icon_class="glyphicon glyphicon glyphicon-tint",
            button_class="btn btn-info")
        action.put()
        return action


class Hunt(Action):

    @staticmethod
    def create():
        action = Action(
            name="hunt", icon_class="glyphicon glyphicon-tree-conifer",
            button_class="btn btn-danger")
        action.put()
        return action


