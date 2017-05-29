from src.producers.building import Building
from src.resources import resource


class Wonder(Building):
    pass


class GreatLibrary(Wonder):

    def get_undiscounted_cost(self):
        return [resource.Gold.create(999999999999999999999999999)]

    def get_discounted_cost(self):
        return [resource.Production.create(100000)]

    @staticmethod
    def create(count=0):
        if count > 1:
            count = 1
        ppt = [
            resource.Science.create(count=25)
        ]
        return GreatLibrary(
            count=count, resource_type="building",
            ticks_per_day=60 * 24,
            production_per_tick=ppt,
            size_per_building=50)
