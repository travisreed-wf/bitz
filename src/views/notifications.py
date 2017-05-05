from flask import request
from flask.views import MethodView
from google.appengine.ext import ndb

from src.notifications.notification import Notification


class MarkAsRead(MethodView):

    def put(self):
        notification_ids = request.get_json()
        notifications = []

        for notification_id in notification_ids:
            notification = Notification.get_by_id(notification_id)
            notification.is_read = True
            notifications.append(notification)

        ndb.put_multi(notifications)
        return 'Success'


def setup_urls(app):

    app.add_url_rule('/notifications/mark_as_read/',
                     view_func=MarkAsRead.as_view('mark_as_read'))
