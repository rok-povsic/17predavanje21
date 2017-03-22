from google.appengine.ext import ndb


class Sporocilo(ndb.Model):
    vnos = ndb.StringProperty()
    ime = ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)