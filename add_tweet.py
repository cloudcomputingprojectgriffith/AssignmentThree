import os

import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

from TweetsModel import tweets_Model

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class add_tweet(webapp2.RequestHandler):

    def post(self):

        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        user = users.get_current_user()
        if action == 'Add':
            addTweetdb = self.request.get('tweet_input')

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if addTweetdb == '':
                self.redirect('/')

            tweetM = tweets_Model(id=myuser.userName + addTweetdb)
            tweetM.tweet.append(addTweetdb)
            tweetM.user = myuser.userName
            tweetM.put()
            self.redirect('/')
