import requests

from src.settings import Settings
from src.workers.worker import Player


class Habitica(object):

    @staticmethod
    def update_habit(resource_name, resource_count, reason=''):
        user = Settings.get_setting_value("HABITICA_USER")
        p = Settings.get_setting_value("HABITICA_TOKEN")
        headers = {
            'x-api-user': user,
            'x-api-key': p
        }

        url = 'https://habitica.com/api/v3/tasks/%s/score/up' % resource_name
        data = {
            'scoreNotes': reason
        }

        player = Player.query().get()
        resource = player.get_resource_by_name(resource_name)
        c = resource.count - resource_count
        unaccounted_for = float(c) % resource.habitica_ratio
        resource_count += unaccounted_for

        for count in xrange(0, int(resource_count)):
            requests.post(url, headers=headers, data=data)
