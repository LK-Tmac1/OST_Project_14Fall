import webapp2, py.jinjaprint as jinjaprint
from google.appengine.api import users
from google.appengine.ext import ndb

class HomePage(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        jinjaprint.header(self,jinjaprint.TITLE_HOME)
        jinjaprint.left_nav(self)
        if current_user:
            jinjaprint.return_message(self, jinjaprint.MESSAGE_WELCOME_BACK+str(current_user))
        else:
            jinjaprint.return_message(self, jinjaprint.MESSAGE_HELLO_GUEST)
        
        jinjaprint.content_end(self)
        jinjaprint.footer(self)


app = webapp2.WSGIApplication([
    ('/.*', HomePage)
    ,(jinjaprint.URL_HOME, HomePage)
], debug=True)
