from copy import copy

from google.appengine.ext import ndb
from src.resources.resource import Health


class Action(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    icon_class = ndb.StringProperty(indexed=False)
    button_class = ndb.StringProperty(indexed=False)

    def perform(self, tile, worker, clicks):
        func = "self._%s(tile, worker, clicks)" % self.name
        return eval(func)

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
    def get_gather_water_action():
        return Action(
            name="gather_water", icon_class="glyphicon glyphicon glyphicon-tint",
            button_class="btn btn-info"
        )

    @staticmethod
    def get_gather_rocks_action():
        return Action(
            name="gather_rocks",
            icon_class="glyphicon glyphicon glyphicon-picture",
            button_class="btn btn-primary"
        )

    def _gather_food(self, tile, worker, clicks):
        produced_food = copy(tile.get_resource_production("Food"))
        produced_food.count = produced_food.count * clicks

        worker_bucket = None
        consumed_resources = []
        produced_resources = [produced_food]
        for worker_resource in worker.resources:
            if worker_resource.name == "Bucket" and worker_resource.count >= 1:
                worker_bucket = worker_resource

        if worker_bucket:
            produced_food.count = produced_food.count * 3
        worker.add_resource(produced_food)

        for produced_resource in produced_resources:
            tile.consume_resource(produced_resource)
        return produced_resources, consumed_resources

    def _gather_wood(self, tile, worker, clicks):
        if tile.building == "Lumberyard":
            clicks = clicks * 2

        produced_wood = copy(tile.get_resource_production("Wood"))
        produced_wood.count = produced_wood.count * clicks

        worker_axe = None
        consumed_resources = []
        produced_resources = [produced_wood]
        for worker_resource in worker.resources:
            if worker_resource.name == "Axe" and worker_resource.count >= 1:
                worker_axe = worker_resource

        if worker_axe:
            worker_axe.count -= 1 * clicks
            consumed_axe = copy(worker_axe)
            consumed_axe.count = 1 * clicks
            consumed_resources.append(consumed_axe)
            produced_wood.count = produced_wood.count * 3
        else:
            consumed_health = Health.create()
            consumed_health.count = 1 * clicks
            consumed_resources.append(consumed_health)
            worker.remove_resource(consumed_health)
        worker.add_resource(produced_wood)

        for produced_resource in produced_resources:
            tile.consume_resource(produced_resource)
        return produced_resources, consumed_resources

    def _gather_rocks(self, tile, worker, clicks):
        produced_rock = copy(tile.get_resource_production("Rock"))
        produced_rock.count = produced_rock.count * clicks

        worker_axe = None
        consumed_resources = []
        produced_resources = [produced_rock]
        for worker_resource in worker.resources:
            if worker_resource.name == "Axe" and worker_resource.count >= 1:
                worker_axe = worker_resource

        if worker_axe:
            worker_axe.count -= 1 * clicks
            consumed_axe = copy(worker_axe)
            consumed_axe.count = 1 * clicks
            consumed_resources.append(consumed_axe)
            produced_rock.count = produced_rock.count * 3
        worker.add_resource(produced_rock)

        for produced_resource in produced_resources:
            tile.consume_resource(produced_resource)
        return produced_resources, consumed_resources

    def _gather_water(self, tile, worker, clicks):
        produced_water = copy(tile.get_resource_production("Water"))
        produced_water.count = produced_water.count * clicks

        worker_bucket = None
        consumed_resources = []
        produced_resources = [produced_water]
        for worker_resource in worker.resources:
            if worker_resource.name == "Bucket" and worker_resource.count >= 1:
                worker_bucket = worker_resource

        if worker_bucket:
            produced_water.count = produced_water.count * 20
        worker.add_resource(produced_water)

        for produced_resource in produced_resources:
            tile.consume_resource(produced_resource)
        return produced_resources, consumed_resources
