import os
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime
from User_Model import MyUser
from TweetsModel import tweets_Model
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class update_Profile_Details(webapp2.RequestHandler):
    Name = ""
    TweeetsRange = 0

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        global Name

        Name = self.request.get('username')

        myuser = MyUser.query(MyUser.userName == Name.lower()).get()

        myuser_key = ndb.Key('MyUser', user.user_id())
        my_user = myuser_key.get()

        userModel_key = ndb.Key('tweets_Model', my_user.userName)

        userProfile = userModel_key.get()

        # TweeetsRange = range(len(userProfile.tweet))

        template_values = {
            'logout_url': users.create_logout_url(self.request.uri),
            'myuser': myuser,
            'userModel': userProfile,
            'range': userProfile.tweet
        }
        template = JINJA_ENVIRONMENT.get_template('view_Profile.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        if action == 'Cancel':
            self.redirect('/')
