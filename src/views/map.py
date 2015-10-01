from flask import render_template, request
from flask.views import MethodView


class MapView(MethodView):

    def get(self):
        return render_template('map.html')


def setup_urls(app):
    app.add_url_rule('/map/', view_func=MapView.as_view('prlist'))
