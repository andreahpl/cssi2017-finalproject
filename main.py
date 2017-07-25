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
    email = ndb.StringProperty()
    score = ndb.IntegerProperty(default=0)


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
            'login_url': login_url,
        }
        self.response.write(template.render(template_vars))

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
        current_user = users.get_current_user()
        template_vars = {
            'current_user': current_user
        }
        template = jinja_environment.get_template('templates/profile-page.html')
        self.response.write(template.render())
    def post(self):
        current_user = users.get_current_user()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/game-menu', GameMenuHandler),
    ('/profile-page', ProfilePageHandler)
], debug=True)
