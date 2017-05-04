from google.appengine.ext import ndb


class LongIntegerProperty(ndb.StringProperty):
  def _validate(self, value):
    if not isinstance(value, (int, long)):
      raise TypeError('expected an integer, got %s' % repr(value))

  def _to_base_type(self, value):
    return str(value) # Doesn't matter if it's an int or a long

  def _from_base_type(self, value):
    return long(value)  # Always return a long
