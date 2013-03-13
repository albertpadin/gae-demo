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


class Idea(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.TextProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        self.response.write("""
            <html>
                <body>
                    <h1>Hello %(name)s (%(email)s - %(user_id)s)</h1>
                    <img src="/static/images/logo.png" />

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
            """ %{"name": user.nickname(), "email": user.email(), "user_id": user.user_id()})


class SubmitIdeaHandler(webapp2.RequestHandler):
    def post(self):

        idea_title = self.request.get("idea_title")
        idea_description = self.request.get("idea_description")

        new_idea = Idea()
        new_idea.title = idea_title
        new_idea.description = idea_description
        new_idea.put()

        self.redirect("/")



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit-idea', SubmitIdeaHandler)
], debug=True)
