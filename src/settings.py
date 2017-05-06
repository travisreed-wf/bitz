import json
from google.appengine.ext import ndb


class Settings(ndb.Model):
    is_json = ndb.BooleanProperty(default=False)
    name = ndb.StringProperty(required=True)
    value = ndb.GenericProperty(indexed=False)

    @staticmethod
    def get_setting_value(name):
        setting = Settings.query(Settings.name == name).get()
        value = setting.value if setting else None
        if value is None:
            return None

        if setting.is_json:
            value = json.loads(value)

        return value
