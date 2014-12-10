import webapp2
import os
import urllib
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('html'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class HomePage(webapp2.RequestHandler):
    def get(self):
    	#self.response.write('LOL.')
     	template = JINJA_ENVIRONMENT.get_template("homepage_header.html")
        self.response.write(template.render())
        #footer = JINJA_ENVIRONMENT.get_template('footer.html')
		#self.response.write(footer.render())



class TestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('For testing.')

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/test', TestHandler)
], debug=True)































