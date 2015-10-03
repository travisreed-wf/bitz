from flask import render_template, request
from flask.views import MethodView
import traceback
import json

from src.locations.location import Location
from src.resources import resource
from src.workers.worker import Player

class BuildToolsView(MethodView):

    def put(self, tool_name):
        clicks = int(request.args.get('clicks'))

        try:
            player = Player.get_by_id("Travis Reed")
            action = "resource.%s.build(worker, count=clicks)" % tool_name
            gained_resources, used_resources = eval(action)
            player.put()
        except:
            print traceback.format_exc()
            return "Failed", 500

        return json.dumps({
            'gained_resources': {r.name: r.count for r in gained_resources},
            'used_resources': {r.name: r.count for r in used_resources}
        })


def setup_urls(app):
    app.add_url_rule('/build/tools/<tool_name>/',
                     view_func=BuildToolsView.as_view('clicks'))
