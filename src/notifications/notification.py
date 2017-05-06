from google.appengine.ext import ndb
from src.workers.worker import Player


class Notification(ndb.model.Model):
    player_key = ndb.KeyProperty(kind=Player, indexed=True)
    message = ndb.StringProperty(indexed=False)
    time = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    is_read = ndb.BooleanProperty(indexed=False, default=False)
    icon_path = ndb.StringProperty(indexed=False)
    title = ndb.StringProperty(indexed=False)

    @property
    def name(self):
        return self._class_name()

    @staticmethod
    def create_new_follower_notification(player_key, follower_name, reason):
        icon_path = 'followers/%s.png' % follower_name
        message = 'Congrats! You have earned a new %s because %s' % (
            follower_name, reason)
        notification = Notification(player_key=player_key, icon_path=icon_path,
                                    message=message, title='New Great Follower')
        notification.put()

    @staticmethod
    def create_new_earned_resource_notification(player_key, resource_name,
                                                resource_count):
        icon_path = 'resources/%s.png' % resource_name
        message = 'Congrats! You have earned %s new %s' % (
            resource_count, resource_name)
        notification = Notification(player_key=player_key, icon_path=icon_path,
                                    message=message,
                                    title='New Earned Resource')
        notification.put()


def create_new_follower_notification(player_key, follower_name, reason):
    Notification.create_new_follower_notification(player_key, follower_name,
                                                  reason)


def create_new_earned_resource_notification(
        player_key, resource_name, resource_count):
    Notification.create_new_earned_resource_notification(
        player_key, resource_name, resource_count)
