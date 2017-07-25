import webapp2
import os
import jinja2

# Import the database API.
from google.appengine.ext import ndb

# Import the user built-in API.
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# This is our model for our user.
class User(ndb.Model):
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    age = ndb.IntegerProperty()

# This is our model for our questions.
class Question(ndb.Model):
    questionText = ndb.StringProperty()
    answer = ndb.StringProperty()
    category = ndb.StringProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):

        template = jinja_environment.get_template('templates/homepage.html')

        # Creates the user login.
        current_user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/')

        # This dictionary stores the variables.
        template_vars = {
            'current_user': current_user,
            'logout_url': logout_url,
            'login_url': login_url
        }
        self.response.write(template.render(template_vars))
        
    def post(self):
        # 1. Get information from API and saves it to database.
        current_user = str(users.get_current_user())
        email = str(current_user)

        #2. Create a user.
        user = User(email=email)

        user.put()

        #3. Create a response.
        self.redirect('/')

class GameMenuHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/game-menu.html')
        self.response.write(template.render())

class GameHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/game-page.html')
        self.response.write(template.render())

class ProfilePageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/profile-page.html')
        self.response.write(template.render())



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/game-menu', GameMenuHandler),
    ('/profile-page', ProfilePageHandler)
], debug=True)
