import json

from flask import render_template, request
from flask.views import MethodView

from src.technologies.technology import Technology
from src.workers.worker import Player


class TechnologiesView(MethodView):

    def get(self):
        player = Player.get_by_id("Travis Reed")
        techs = Technology.query(
            Technology.can_research == True,
            Technology.is_researched == False).fetch()

        return render_template(
            'technologies.html', player=player, techs=techs)

    def post(self):
        player = Player.get_by_id("Travis Reed")
        tech_name = request.get_json()['technology']
        cls = Technology.get_cls_by_name(tech_name)
        tech = cls.get_by_player(player)
        cost = tech.research(player)

        return json.dumps({
            'used_resources': {r.name: r.count for r in cost},
            'gained_resources': {}
        })


def setup_urls(app):
    app.add_url_rule('/technologies/', view_func=TechnologiesView.as_view(
        'technologies'))
