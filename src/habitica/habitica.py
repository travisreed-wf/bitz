import requests

from src.settings import Settings


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
        for count in xrange(0, resource_count):
            requests.post(url, headers=headers, data=data)
