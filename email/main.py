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


class Idea(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    votes = ndb.IntegerProperty(default=0)
    email = ndb.StringProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        ideas = Idea.query().order(-Idea.votes).fetch(20)

        self.response.write("""
            <html>
                <body>
                    <h1>Hello %(name)s (%(email)s - %(user_id)s)</h1>
                    <img src="/static/images/logo.png" />

            """ %{"name": user.nickname(), "email": user.email(), "user_id": user.user_id()})


        self.response.out.write("<h2>Ideas</h2>")

        for idea in ideas:
            self.response.out.write("""

                <div style="font-size: 30px;">
                    <div>%(idea_title)s</div>
                    <div>%(idea_description)s</div>
                    <div>%(idea_votes)s votes</div>
                    <form action="/vote-idea" method="POST">
                        <input type="hidden" name="idea_id" value="%(idea_id)s" />
                        <button type="submit" style="font-size: 30px;">Vote</button>
                    </form>
                </div>
                <hr />

                """ %{
                "idea_title": idea.title,
                "idea_description": idea.description,
                "idea_votes": idea.votes,
                "idea_id": str(idea.key.id())}
                )



        self.response.out.write("""
            <h2>Submit an Idea</h2>

            <form action="/submit-idea" method="POST">
                <input type="text" name="idea_title" placeholder="Enter Title" style="font-size: 50px;" />
                <br /><br />

                <textarea name="idea_description" placeholder="Enter Description" style="font-size: 50px;"></textarea>
                <br /><br />

                <button type="submit" style="font-size: 50px;">Submit Idea</button>
            </form>
        </body>
    </html>
            """)


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
