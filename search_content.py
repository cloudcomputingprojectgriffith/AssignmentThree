import os

import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

from TweetsModel import tweets_Model
from User_Model import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class search_Content(webapp2.RequestHandler):

    def post(self):

        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        user = users.get_current_user()

        if action == 'search':
            temp = []
            response = []

            result = self.request.get('word')

            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if result == '':
                self.redirect('/')
            else:
                username_search = MyUser.query(MyUser.userName == result).fetch()
                tweet_search = tweets_Model.query().fetch()

                if len(username_search) > 0 or len(tweet_search) > 0:

                    for tweet in tweet_search:
                        for i in tweet.tweet:
                            temp.append(i)
                    for i in range(len(temp)):
                        s1 = temp[i].split(" ")
                        for x in s1:
                            if (x in result):
                                response.append(temp[i])
                                break;

                    template_values = {
                        'tweet_search': response,
                        'username_search': username_search,
                        'myuser': myuser,
                    }
                    template = JINJA_ENVIRONMENT.get_template('main_page.html')
                    self.response.write(template.render(template_values))
