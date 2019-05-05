from google.appengine.ext import ndb;


class tweets_Model(ndb.Model):
    user = ndb.StringProperty()
    tweet = ndb.StringProperty(repeated=True)
    timestamp = ndb.DateTimeProperty(auto_now=True)
