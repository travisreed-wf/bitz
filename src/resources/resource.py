from google.appengine.ext import ndb


class Resource(polymodel.PolyModel):
    name = ndb.StringProperty()
    count = ndb.IntegerProperty(indexed=False)


class Dollar(Resource):
    pass

class Food(Resource):
    pass

class Gold(Resource):
    pass

class Health(Resource):
    pass

class Iron(Resource):
    pass

class Wood(Resource):
    pass
