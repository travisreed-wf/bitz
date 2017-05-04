from flask import request
from flask.views import MethodView
import traceback

from src.external_data import external_data
from src.resources import resource
from src.workers.worker import Player


class ClashWinsView(MethodView):

    def __init__(self):
        self.new_count = 0
        self.player = None

    def post(self):
        self.new_count = int(request.args.get('count'))

        try:
            self.player = Player.get_by_id("Travis Reed")
            self._update_wins()
        except:
            print traceback.format_exc()
            return "Failed", 500

        return str(self.player.get_resource_by_name(
            'ClashRoyaleWins').count), 200

    def _update_wins(self):
        current = external_data.ClashRoyaleData.get_previous_entity()
        if current:
            current_count = current.count
        else:
            current_count = 0
        new = external_data.ClashRoyaleData(count=self.new_count)
        new.put()
        r = resource.ClashRoyaleWins.create(count=(new.count - current_count))
        self.player.add_resource(r)


def setup_urls(app):
    app.add_url_rule('/extension/clash_wins/',
                     view_func=ClashWinsView.as_view('clash_wins'))
