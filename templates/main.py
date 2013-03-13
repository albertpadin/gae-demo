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

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail


import jinja2
import os

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), autoescape=True)


class Idea(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    votes = ndb.IntegerProperty(default=0)
    email = ndb.StringProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        ideas = Idea.query().order(-Idea.votes).fetch(20)

        template_variables = {
            "user": user,
            "ideas": ideas
        }

        template = jinja_environment.get_template("frontend/front2.html")
        self.response.out.write(template.render(template_variables))



class SubmitIdeaHandler(webapp2.RequestHandler):
    def post(self):

        idea_title = self.request.get("idea_title")
        idea_description = self.request.get("idea_description")

        new_idea = Idea()
        new_idea.title = idea_title
        new_idea.description = idea_description
        new_idea.email = users.get_current_user().email()
        new_idea.put()

        self.redirect("/")


class VoteIdeaHandler(webapp2.RequestHandler):
    def post(self):

        idea_id = int(self.request.get("idea_id"))

        idea = Idea.get_by_id(idea_id)

        if idea:
            idea.votes += 1
            idea.put()

        if idea.email:
            mail.send_mail(sender="albertpadin@gmail.com>",
                            to=str(idea.email),
                            subject= "Congratulations!!",
                            body="Your idea got a vote!")


        self.redirect("/")



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit-idea', SubmitIdeaHandler),
    ('/vote-idea', VoteIdeaHandler)
], debug=True)
