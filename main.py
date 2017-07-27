import webapp2
import os
import jinja2
import json
import logging
import random


# Import the database API.
from google.appengine.ext import ndb

# Import the user built-in API.
from google.appengine.api import users

# Import the API to fetch data from url.
from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def read_questions():
    # 1. Access the url to get the results.
    url = 'https://opentdb.com/api.php?amount=100'
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

    return items

def pass_questions(items):
    for item in items:
        # 1. Get the questions, the correct answer, and the incorrect
        # answers.
        question_text = item['question']
        correct_answer = item['correct_answer']
        incorrect_answers = item['incorrect_answers']

        # 2. Store this information into a question model.
        question = Question(
                   question_text=question_text,
                   correct_answer=correct_answer,
                   incorrect_answers=incorrect_answers)

        # 3. Save question into the database.
        question.put()


# Make a questions class.
class Question(ndb.Model):
    question_text = ndb.StringProperty()
    correct_answer = ndb.StringProperty()
    incorrect_answers = ndb.StringProperty(repeated=True)

# Make a photos class.
class Photo(ndb.Model):
    photo_url = ndb.StringProperty()
    correct_answer = ndb.StringProperty()
    incorrect_answers = ndb.StringProperty(repeated=True)


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

        questions = Question.query().fetch()

        # If there are no questions in the database, add defaults.
        # This will only happen one time (on the first run).
        if not questions:
            questions = pass_questions(read_questions())
        # This dictionary stores the variables.
        template_vars = {
            'current_user': current_user,
            'logout_url': logout_url,
            'login_url': login_url,
            'questions': questions
        }
        self.response.write(template.render(template_vars))

class GameMenuHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/game-menu.html')
        self.response.write(template.render())

class GamePageHandler(webapp2.RequestHandler):
    def get(self):
        # Query and Fetch 10 random questions.
        question_query = Question.query()
        questions = question_query.fetch()


        # Randomized set of 10 questions.
        random_set_10=[]
        question_list = random.sample(questions, 10)
        for question in question_list:
            answers = question.incorrect_answers
            answers.append(question.correct_answer)
            random.shuffle(answers)
            random_set_10.append(
            {
            'question': question.question_text,
            'answers': answers,
            'question_key': question.key.urlsafe()
            }
            )

        # This dictionary stores the variables.
        game_page_vars = {
        'questions': random_set_10
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

class LeaderboardHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/leaderboard.html')
        self.response.write(template.render())

class SubmitQuestionsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/submit-questions.html')
        self.response.write(template.render())
    def post(self):
        question_text = self.request.get('question_text')
        correct_answer = self.request.get('correct_answer')
        incorrect_answers = self.request.get('incorrect_answers')
        new_question = Question(question_text=question_text, correct_answer=correct_answer, incorrect_answers=incorrect_answers)
        new_question.put()
        self.redirect("/")

class ScoreHandler(webapp2.RequestHandler):
    def post(self):

        q_key = self.request.get('question_key')
        answer = self.request.get('answer')

        # TODO: Check if the answer is correct, if so update the score.

        print q_key, answer



        # TODO: Later, possibly return the score.
        # self.response.write

        # Handles increasing the scores when you click the button.
                # === 1: Get info from the request. ===
        # urlsafe_key = self.request.get('photo_key')
        #
        # # === 2: Interact with the database. ===
        #
        # # Use the URLsafe key to get the photo from the DB.
        # photo_key = ndb.Key(urlsafe=urlsafe_key)
        # photo = photo_key.get()
        #
        # # Fix the photo like count just in case it is None.
        # if photo.like_count == None:
        #     photo.like_count = 0
        #
        # # Increase the photo count and update the database.
        # photo.like_count = photo.like_count + 1
        # photo.put()
        #
        # # === 3: Send a response. ===
        # # Send the updated count back to the client.
        # self.response.write(photo.like_count)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/game-menu', GameMenuHandler),
    ('/game-page', GamePageHandler),
    ('/profile-page', ProfilePageHandler),
    ('/leaderboard', LeaderboardHandler),
    ('/submit-questions', SubmitQuestionsHandler),
    ('/score', ScoreHandler)
], debug=True)
