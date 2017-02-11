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

class MainPage(Handler):
    """Handles incoming requests to '/'"""

    def get(self):
        """Handles incoming GET requests"""

        self.render('base.html')

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
