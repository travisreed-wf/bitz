from flask import render_template, request
from flask.views import MethodView
import traceback
import json

from src.locations.location import Location
from src.workers.worker import Player


class ClicksView(MethodView):

    def put(self, location_id, tile_index, action_name):
        clicks = int(request.args.get('clicks'))
        location = Location.get_by_id(location_id)
        if not location:
            return "Invalid location", 404

        tile = location.tiles[int(tile_index)].get()
        try:
            player = Player.get_by_id("Travis Reed")
            gained_resources, used_resources = tile.perform_action(
                action_name, player, clicks)
            player.put()
        except:
            print traceback.format_exc()
            return "Failed", 500

        return json.dumps({
            'gained_resources': {r.name: r.count for r in gained_resources},
            'used_resources': {r.name: r.count for r in used_resources}
        })


def setup_urls(app):
    app.add_url_rule('/map/<location_id>/<tile_index>/<action_name>/',
                     view_func=ClicksView.as_view('clicks'))
