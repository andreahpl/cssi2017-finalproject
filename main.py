import webapp2
import os
import jinja2
import json
import logging

# Import the database API.
from google.appengine.ext import ndb

# Import the user built-in API.
from google.appengine.api import users

from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# Make a questions class.
class Question(ndb.Model):
        question_text = ndb.StringProperty()
        correct_answer = ndb.StringProperty()
        incorrect_answers = ndb.StringProperty()

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

class GamePageHandler(webapp2.RequestHandler):
    def get(self):
        # 1. Access the url to get the results.
        url = 'https://opentdb.com/api.php?amount=10'
        try:
            result = urlfetch.fetch(url)
            if result.status_code != 200:
                self.response.status_code = result.status_code
                return

        # 2. If something incorrect happens when fetching url, then it returns
        # a status code and logs the error.
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
            self.response.status_code = 500
            return

        # 3. Converts from JSON object to a python object and gets the result
        # list.
        items = json.loads(result.content)['results']

        for item in items:
            # 1. Get the questions, the correct answer, and the incorrect
            # answers.
            question = item['question']
            correct_answer = item['correct_answer']
            incorrect_answers = item['incorrect_answers']

            # 2. Make one randomized answers list with both the correct and
            # incorrect answers.
            answers = []
            answers.append(correct_answer)
            answers.append(incorrect_answers)

        game_page_vars = {
            'items': items
        }

        template = jinja_environment.get_template('templates/game-page.html')
        self.response.write(template.render(game_page_vars))

class ProfilePageHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        template_vars = {
            'current_user': current_user
        }
        template = jinja_environment.get_template('templates/profile-page.html')
        self.response.write(template.render(template_vars))
    def post(self):
        current_user = users.get_current_user()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/game-menu', GameMenuHandler),
    ('/game-page', GamePageHandler),
    ('/profile-page', ProfilePageHandler)
], debug=True)
