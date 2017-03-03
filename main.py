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

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    """Class to simplify other functions"""

    def write(self, *a, **kw):
        """Method to shorten write function"""

        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        """Renders template"""

        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """renders template"""

        self.write(self.render_str(template, **kw))

class BlogPost(db.Model):
    """Class to create BlogPost database"""

    title = db.StringProperty(required=True)
    post = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    date = db.DateProperty(auto_now_add=True)

class MainBlog(Handler):
    """Handles incoming requests to '/mainblog' """

    def render_mainblog(self, title="", post="", error="", date=""):
        """Renders mainblog.html"""

        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 5")
        self.render("mainblog.html", error=error, title=title, post=post, posts=posts, date=date)

    def get(self):
        """Handles incoming GET requests"""

        self.render_mainblog()


class NewPost(Handler):
    """Handles incoming requests to '/newpost' """

    def render_newpost(self, title="", post="", error="", date=""):
        """Renders newpost.html"""

        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 5")
        self.render("newpost.html", error=error, title=title, post=post, posts=posts, date=date)

    def get(self):
        """Handles incoming get requests"""

        self.render_newpost()

    def post(self):
        """Handles incoming post requests"""

        title = self.request.get("title")
        post = self.request.get("post")

        if title and post:
            entry = BlogPost(title=title, post=post)
            entry.put()

            self.redirect("/blog/" + str(entry.key().id()))
        else:
            error = "Please provide both a title and a post!"
            self.render_newpost(title, post, error)

class ViewPostHandler(Handler):
    """Dynamic handler for dealing with new post pages"""

    def renderError(self, error):
        """ Sends an HTTP error code and a generic "oops!" message to the client. """

        self.response.write(error)

    def get(self, id):
        """Hanldes get requests for new post pages"""

        post = BlogPost.get_by_id(int(id))

        if not post:
            self.renderError("Error: That Post Does Not Exist!!")
        else:
            self.render("completedpost.html", post=post)

app = webapp2.WSGIApplication([
    ('/mainblog', MainBlog),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
