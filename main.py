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
    url = 'https://opentdb.com/api.php?amount=50'
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
    current_score = ndb.IntegerProperty(default=0)
    image_high_score = ndb.IntegerProperty(default=0)
    current_image_score = ndb.IntegerProperty(default=0)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/homepage.html')

        # Creates the user login.
        current_user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/')

        questions = Question.query().fetch()
        photos = Photo.query().fetch()

        # If there are no questions in the database, add defaults.
        # This will only happen one time (on the first run).
        if not questions:
            questions = pass_questions(read_questions())

        if not photos:
            with open("image_questions.json") as f:
                photos = json.load(f)
                for photo in photos:
                    picture = Photo(**photo)
                    picture.put()
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
        # Allows user to logout
        logout_url = users.create_logout_url('/')
        template_vars = {
            'logout_url': logout_url,
        }
        self.response.write(template.render(template_vars))

class GamePageHandler(webapp2.RequestHandler):
    def get(self):
        # Query and Fetch 10 random questions.
        question_query = Question.query()
        questions = question_query.fetch()

        current_user_email = users.get_current_user().email()

        user_query = User.query(User.email == current_user_email)
        user = user_query.get()

        if not user:
            user = User(email=current_user_email)
            user.put()

        user.current_score = 0
        user.put()


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
            'questions': random_set_10,
            "user": user,
        }

        template = jinja_environment.get_template('templates/game-page.html')
        self.response.write(template.render(game_page_vars))
    def post(self):
        current_user_email = users.get_current_user().email()
        user_query = User.query(User.email == current_user_email)
        user = user_query.get()

        q_key_url = self.request.get('question_key')
        answer = self.request.get('answer')

        q_key = ndb.Key(urlsafe=q_key_url)

        # TODO: Check if the answer is correct, if so update the score.
        correct_answer = q_key.get().correct_answer

        if answer == correct_answer:

            user.current_score += 1
            user.put()

            if user.current_score > user.score:
                user.score = user.current_score
                user.put()

class ImagePageHandler(webapp2.RequestHandler):
    def get(self):
        # Query and Fetch 10 random questions.
        photo_query = Photo.query()
        photos = photo_query.fetch()

        current_user_email = users.get_current_user().email()

        user_query = User.query(User.email == current_user_email)
        user = user_query.get()

        if not user:
            user = User(email=current_user_email)
            user.put()

        user.current_image_score = 0
        user.put()


        # Randomized set of 10 questions.
        random_set_10=[]
        photo_list = random.sample(photos, 10)
        for photo in photo_list:
            answers = photo.incorrect_answers
            answers.append(photo.correct_answer)
            random.shuffle(answers)
            random_set_10.append(
            {
            'photo': photo.photo_url,
            'answers': answers,
            'photo_key': photo.key.urlsafe()
            }
            )

        # This dictionary stores the variables.
        image_page_vars = {
            'photos': random_set_10,
            "user": user,
        }

        template = jinja_environment.get_template('templates/image_page.html')
        self.response.write(template.render(image_page_vars))
    def post(self):
        current_user_email = users.get_current_user().email()
        user_query = User.query(User.email == current_user_email)
        user = user_query.get()

        p_key_url = self.request.get('photo_key')
        answer = self.request.get('answer')

        p_key = ndb.Key(urlsafe=p_key_url)

        # TODO: Check if the answer is correct, if so update the score.
        correct_answer = p_key.get().correct_answer

        if answer == correct_answer:

            user.current_image_score += 1
            user.put()

            if user.current_image_score > user.image_high_score:
                user.image_high_score = user.current_image_score
                user.put()



class ProfilePageHandler(webapp2.RequestHandler):
    def get(self):
        current_user_email = users.get_current_user().email()
        # Find the user entity where the entity's email matches the current user's email
        user_query = User.query(User.email == current_user_email)
        user = user_query.get()

        current_user = users.get_current_user()
        template_vars = {
            'current_user': current_user,
            'user': user,
        }
        template = jinja_environment.get_template('templates/profile-page.html')
        self.response.write(template.render(template_vars))

class LeaderboardHandler(webapp2.RequestHandler):
    def get(self):
        user_query = User.query().order(-User.score)
        user_image_query = User.query().order(-User.image_high_score)
        users = user_query.fetch()
        users2 = user_image_query.fetch()

        template_vars = {
            'users': users,
            'users2': users2,
        }
        template = jinja_environment.get_template('templates/leaderboard.html')
        self.response.write(template.render(template_vars))

class SubmitQuestionsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/submit-questions.html')
        self.response.write(template.render())
    def post(self):
        question_text = self.request.get('question_text')
        correct_answer = self.request.get('correct_answer')
        # Turns user input into a string
        incorrect_answers = str(self.request.get('incorrect_answers'))
        # Turns the string into a list
        incorrect_answers_list = incorrect_answers.split(',')
        new_question = Question(question_text=question_text, correct_answer=correct_answer, incorrect_answers=incorrect_answers_list)
        new_question.put()
        self.redirect("/game-menu")

class ScoreHandler(webapp2.RequestHandler):
    def post(self):
        current_user_email = users.get_current_user().email()
        # Find the user entity where the entity's email matches the current user's email
        user_query = User.query(User.email == current_user_email)
        user = user_query.get()

        q_key_url = self.request.get('question_key')
        answer = self.request.get('answer')

        q_key = ndb.Key(urlsafe=q_key_url)

        # TODO: Check if the answer is correct, if so update the score.
        correct_answer = q_key.get().correct_answer

        if answer == correct_answer:
            user.current_score += 1
            user.put()

            if user.current_score > user.score:
                user.score = user.current_score
                user.put()
        response = {
            "score": user.current_score,
            "correct": answer == correct_answer,
        }

        self.response.write(json.dumps(response))

class ImageScoreHandler(webapp2.RequestHandler):
    def post(self):
        current_user_email = users.get_current_user().email()
        # Find the user entity where the entity's email matches the current user's email
        user_query = User.query(User.email == current_user_email)
        user = user_query.get()

        p_key_url = self.request.get('photo_key')
        answer = self.request.get('answer')

        p_key = ndb.Key(urlsafe=p_key_url)

        # TODO: Check if the answer is correct, if so update the score.
        correct_answer = p_key.get().correct_answer

        if answer == correct_answer:
            user.current_image_score += 1
            user.put()

            if user.current_image_score > user.image_high_score:
                user.image_high_score = user.current_image_score
                user.put()
        response2 = {
            "score": user.current_image_score,
            "correct": answer == correct_answer,
        }

        self.response.write(json.dumps(response2))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/game-menu', GameMenuHandler),
    ('/game-page', GamePageHandler),
    ('/profile-page', ProfilePageHandler),
    ('/leaderboard', LeaderboardHandler),
    ('/submit-questions', SubmitQuestionsHandler),
    ('/score', ScoreHandler),
    ('/image-page', ImagePageHandler),
    ('/image-score', ImageScoreHandler)
], debug=True)
