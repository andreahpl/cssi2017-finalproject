#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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

class MainHandler(webapp2.RequestHandler):
    def get(self):

        template = jinja_environment.get_template("templates/homepage.html")

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

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
