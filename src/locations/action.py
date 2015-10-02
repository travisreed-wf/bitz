from copy import copy

from google.appengine.ext import ndb


class Action(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    icon_class = ndb.StringProperty(indexed=False)
    button_class = ndb.StringProperty(indexed=False)

    def perform(self, worker_resources, clicks):
        func = "self._%s(worker_resources, clicks)" % self.name
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


    def _gather_wood(self, worker_resources, clicks):
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
            self.consume_resource(produced_resource)
        return produced_resources, consumed_resources
