from datetime import datetime, timedelta
import json
import logging

from flask.views import MethodView
from google.appengine.ext import ndb

from src.workers.worker import Worker

class MinuteCron(MethodView):

    def get(self):
        MinuteCron._check_basic_needs()

        return 'Success', 200

    @staticmethod
    def _check_basic_needs():
        workers = Worker.query().fetch()
        for worker in workers:
            worker.check_basic_needs()

def setup_urls(app):
    app.add_url_rule('/crons/minute/',
                     view_func=MinuteCron.as_view('crons.minute'))
