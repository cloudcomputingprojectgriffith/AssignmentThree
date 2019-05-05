from datetime import datetime
import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from User_Model import MyUser
from google.appengine.api import users
from TweetsModel import tweets_Model
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class edit_Profile_Details(webapp2.RequestHandler):
    Name = ""

    def get(self):
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        Name = ""
        global Name
        Name = self.request.get('username')

        myuser_key = ndb.Key('MyUser', user.user_id())
        my_user = myuser_key.get()

        myuser = MyUser.query(MyUser.userName == Name).get()

        userModel_key = ndb.Key('tweets_Model', my_user.userName)

        userProfile = userModel_key.get()

        template_values = {
            'logout_url': users.create_logout_url(self.request.uri),
            'myuser': myuser,
            'userModel': userProfile,
            'range': len(userProfile.tweet)
        }
        template = JINJA_ENVIRONMENT.get_template('edit_details.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        if action == 'update':

            myuser = MyUser.query(MyUser.userName == Name).get()

            myuser.userName = self.request.get('userName')
            myuser.bio = self.request.get('bio')
            myuser.email = self.request.get('email')

            myuser.put()

            self.redirect('/')


        elif self.request.get('button') == 'Cancel':
            self.redirect('/')
