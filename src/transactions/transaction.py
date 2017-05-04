from google.appengine.ext import ndb
from google.appengine.ext.ndb import model

from src.helpers import LongIntegerProperty


class Transaction(model.Model):
    count = ndb.FloatProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    description = ndb.StringProperty()
