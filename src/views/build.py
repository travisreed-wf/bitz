from flask import render_template, request
from flask.views import MethodView
import traceback
import json

from src.locations.location import Location
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
            print gained_resources, used_resources
            player.put()
        except:
            print traceback.format_exc()
            return "Failed", 500

        return json.dumps({
            'gained_resources': {r.name: r.count for r in gained_resources},
            'used_resources': {r.name: r.count for r in used_resources}
        })


class BuildBuildingView(MethodView):

    def put(self, location_id, tile_index, building_name):
        try:
            location = Location.get_by_id(location_id)
            tile = location.tiles[int(tile_index)].get()
            tile.build_building(building_name)
            player = Player.get_by_id("Travis Reed")

            player.put()
            return "success"
        except:
            print traceback.format_exc()
            return "Failed", 500


def setup_urls(app):
    app.add_url_rule('/build/tools/', view_func=BuildToolsView.as_view('build_tools_get'))
    app.add_url_rule('/build/tools/<tool_name>/',
                     view_func=BuildToolsView.as_view('build_tools_put'))
    app.add_url_rule('/build/<location_id>/<tile_index>/<building_name>/',
                 view_func=BuildBuildingView.as_view('build'))
