from flask import render_template, request
from flask.views import MethodView
import traceback
import json

from src.exceptions import InsufficientResourcesException
from src.locations.location import Location, Tile
from src.locations.map import Earth
from src.producers import building
from src.resources import resource
from src.workers.worker import Player


class BuildToolsView(MethodView):

    def get(self):
        player = Player.get_by_id("Travis Reed")

        return render_template('build_tools.html', player=player)

    def put(self, tool_name):
        clicks = int(request.args.get('clicks'))

        try:
            player = Player.get_by_id("Travis Reed")
            action = "resource.%s.build(player, count=clicks)" % tool_name
            gained_resources, used_resources = eval(action)
            player.put()
        except:
            print traceback.format_exc()
            return "Failed", 500

        return json.dumps({
            'gained_resources': {r.name: r.count for r in gained_resources},
            'used_resources': {r.name: r.count for r in used_resources}
        })


class BuildBuildingOnTileView(MethodView):

    def put(self, tile_id, building_name):
        try:
            tile = Tile.get_by_id(int(tile_id))
            tile.build_building(building_name)
            return "Success"
        except:
            print traceback.format_exc()
            return "Failed", 500


class BuildBuildingsView(MethodView):

    def get(self):
        player = Player.get_by_id("Travis Reed")

        return render_template('build_buildings.html', player=player,
                               map=Earth())

    def post(self):
        data = request.get_json()
        player = Player.get_by_id("Travis Reed")
        class_name = data.get('building')
        count = data.get('count', 1)
        map_class = Earth
        try:
            used_resources = eval(
                'building.%s.build(player, map_class, count=count)' %
                class_name)
            player.put()
        except InsufficientResourcesException as e:
            return e.message, 400

        return json.dumps({
            'used_resources': {r.name: r.count for r in used_resources},
            'gained_resources': {class_name: count}
        })


class BuildBuildingsReactView(MethodView):

    def get(self):
        map = Earth()
        player = Player.get_by_id("Travis Reed")
        serialized_buildings = []
        for b in player.ordered_buildings:
            discounted_cost = {}
            for r in b.get_discounted_cost():
                discounted_cost[r.name] = r.count
            undiscounted_cost = {}
            for r in b.get_undiscounted_cost():
                undiscounted_cost[r.name] = r.count

            serialized_buildings.append({
                "seconds_since_last_tick": b.seconds_since_last_tick,
                "seconds_between_ticks": b.seconds_between_ticks,
                "production_per_tick_dict": b.production_per_tick_dict,
                "total_space_in_use": b.total_space_in_use,
                "name": b.name,
                "ticks_per_day": b.ticks_per_day,
                "discounted_cost": discounted_cost,
                "undiscounted_cost": undiscounted_cost,
                "total_designated_space": b.get_total_designated_space(map),
                "percent_of_cost_available": player.percent_of_cost_available(
                    b.get_cost(map))
            })

        return render_template(
            'build_buildings_2.html', player=player, map=map,
            serialized_buildings=json.dumps(serialized_buildings))


def setup_urls(app):
    app.add_url_rule('/build/tools/',
                     view_func=BuildToolsView.as_view('build_tools_get'))
    app.add_url_rule('/build/tools/<tool_name>/',
                     view_func=BuildToolsView.as_view('build_tools_put'))
    app.add_url_rule('/build/<tile_id>/<building_name>/',
                     view_func=BuildBuildingOnTileView.as_view('build'))

    app.add_url_rule('/build/buildings/', view_func=BuildBuildingsView.as_view(
        'build_buildings'))
    app.add_url_rule(
        '/build/buildings_react/',
        view_func=BuildBuildingsReactView.as_view('react_buildings'))

