import webapp2
import py.constant as constant
from google.appengine.api import users
from google.appengine.ext import ndb

class HomePage(webapp2.RequestHandler):
    def get(self):
        constant.header(self,constant.TITLE_HOME)
        current_user = users.get_current_user()

        if current_user:
            templ_value={
            "user": current_user,
            "logout_url": users.create_logout_url(self.request.uri)
            }
            constant.left_nav(self, constant.USER_MODE, templ_value)
        else:
            templ_value={"login_url":users.create_login_url(self.request.uri)}
            constant.left_nav(self, constant.GUEST_MODE, templ_value)

        constant.view_question_header(self)
        constant.view_question_list(self)

        constant.footer(self)


class Login(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_login_url(self.request.uri))


class Logout(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_logout_url(self.request.uri))


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/login', Login),
    ('/logout', Logout),
], debug=True)































