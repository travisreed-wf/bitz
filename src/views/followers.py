from flask import render_template
from flask.views import MethodView
import json

from src.locations.map import Earth
from src.workers.worker import Player


class FollowersReactView(MethodView):

    def get(self):
        self.map = Earth()
        self.player = Player.get_by_id("Travis Reed")

        return render_template(
            'followers.html', player=self.player, map=self.map,
            organized_resources=json.dumps(self._get_organized_resources()),
            follower_data=json.dumps(self._get_follower_data()))

    def _get_follower_data(self):
        d = {}
        for r in self.player.resources:
            if r.resource_type == 'follower':
                d[r.name] = {
                    'description': r.description
                }
        return d

    def _get_organized_resources(self):
        resource_dict = {}
        for resource_type, resources in \
                self.player.organized_resources.iteritems():
            resource_dict[resource_type] = {}
            for resource in resources:
                resource_dict[resource_type][resource.name] = resource.count
        return resource_dict


def setup_urls(app):
    app.add_url_rule(
        '/followers/',
        view_func=FollowersReactView.as_view('followers.react'))
