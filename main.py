import os

from datetime import datetime
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from User_Model import MyUser
from TweetsModel import tweets_Model
from add_tweet import add_tweet
from search_content import search_Content
from edit_details import edit_Profile_Details
from view_Profile import update_Profile_Details

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class HomePage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('login_app.html')
            self.response.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if myuser == None:
            template_values = {
                'logout_url': users.create_logout_url(self.request.uri),

            }
            template = JINJA_ENVIRONMENT.get_template('register_app.html')
            self.response.write(template.render(template_values))
        else:

            twitter_Model = tweets_Model.query().fetch()

            template_values = {
                'logout_url': users.create_logout_url(self.request.uri),
                'tweet': twitter_Model,
                'myuser': myuser,
            }
            template = JINJA_ENVIRONMENT.get_template('main_page.html')
            self.response.write(template.render(template_values))

    def post(self):

        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        user = users.get_current_user()

        if action == 'signup':
            userName = self.request.get('userName')
            userBio = self.request.get('bio')
            email = self.request.get('email')
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            myuser = MyUser(id=user.user_id(), userName=userName, date=datetime.date(datetime.now()),
                            bio=userBio, email=email)
            myuser.put()

            twitter_Key = ndb.Key('tweets_Model', myuser.userName)
            newTweet = twitter_Key.get()

            newTweet = tweets_Model(id=myuser.userName, user=userName)
            newTweet.put()
            self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/search_content', search_Content),
    ('/add_tweet', add_tweet),
    ('/edit_details', edit_Profile_Details),
    ('/view_Profile', update_Profile_Details)

], debug=True)
