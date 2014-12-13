import webapp2
import py.constant as constant
from py.datamodel import *

from google.appengine.api import users
from google.appengine.ext import ndb


class HomePage(webapp2.RequestHandler):

    def get(self):
        current_user = unicode(users.get_current_user())
        constant.header(self,constant.TITLE_HOME)
        if current_user:
            templ_value={
            constant.HTML_CURRENT_USER: current_user,
            constant.HTML_LOGOUT_URL: users.create_logout_url(self.request.uri)
            }
            constant.left_nav(self, constant.MODE_USER, templ_value)
        else:
            templ_value={constant.HTML_LOGIN_URL:users.create_login_url(self.request.uri)}
            constant.left_nav(self, constant.MODE_GUEST, templ_value)

        constant.view_question_header(self, constant.MODE_VIEW_ALL_Q)
        Qs=Question.get_every_question()
        templ_value={
        constant.HTML_CURRENT_USER: current_user
        ,constant.HTML_LOGOUT_URL: users.create_logout_url(self.request.uri)
        ,constant.HTML_Q_LOOP: Qs
        ,constant.HTML_VIEW_MY_Q: False
        ,constant.HTML_TAG_Q: constant.MODE_TAG_ALL_Q
        }

        constant.view_question_list(self, templ_value)
        constant.footer(self)

    def post(self):
        constant.vote_q(self)
        constant.show_success(self)


class Login(webapp2.RequestHandler):
    def get(self):
        constant.login(self)

class Logout(webapp2.RequestHandler):
    def get(self):
        HomePage(webapp2.RequestHandler).get()
        constant.logout(self)


app = webapp2.WSGIApplication([
    ('/', HomePage)
    ,(constant.URL_HOME, HomePage)
    ,(constant.URL_LOGIN, Login)
    ,(constant.URL_LOGOUT, Logout)
], debug=True)
