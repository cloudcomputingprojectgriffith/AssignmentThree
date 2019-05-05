from google.appengine.ext import ndb
import datetime


class MyUser(ndb.Model):
    userName = ndb.StringProperty()
    date = ndb.DateProperty(default=datetime.datetime.now)
    bio = ndb.StringProperty()
    email = ndb.StringProperty()
    userFollowers = ndb.StringProperty(repeated=True)
    userFollowing = ndb.StringProperty(repeated=True)
