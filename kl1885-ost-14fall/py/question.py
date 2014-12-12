import webapp2
import os
import urllib
import jinja2
import datetime
import py.homepage as homepage
import py.constant as constant
from py.datamodel import *

from google.appengine.api import users
from google.appengine.ext import ndb


class CreateQuestion(webapp2.RequestHandler):
    def get(self):
        constant.header(self,constant.TITLE_CREATE_Q)
        current_user = users.get_current_user()
        if current_user:
            left_nav=constant.JINJA_ENVIRONMENT.get_template(constant.LEFT_NAV_USER_TEMP)
            templ_value={
            "user": current_user,
            "logout_url": users.create_logout_url(self.request.uri)
            }
            self.response.write(left_nav.render(templ_value))
            create_question=constant.JINJA_ENVIRONMENT.get_template(constant.CREATE_Q_TEMP)
            self.response.write(create_question.render(templ_value))

        else:
            self.redirect(users.create_login_url(self.request.uri))

        self.response.write(constant.JINJA_ENVIRONMENT.get_template(constant.FOOTER_TEMP).render())
        constant.footer(self)

    def post(self):
        submit=self.request.get("submit")
        if submit == "Cancel":
            self.redirect("/")
        elif submit == "Submit":
            q_content=str(self.request.get("qcontent"))
            if constant.check_string_empty(q_content):
                constant.invalid_behavior(self, constant.EMPTY_Q_CONTENT_MESSAGE)
            else:
                constant.header(self)
                newQ=Question()
                newQ.q_content=q_content
                if not str(self.request.get("qtags")).isspace():
                    newQ.q_tags=self.request.get("qtags")
                create_time=datetime.datetime.now()
                newQ.create_time=create_time
                newQ.q_id=create_time.strftime("%s")
                newQ.vd_num=0
                newQ.vp_num=0
                
                constant.footer(self)





app = webapp2.WSGIApplication([
    ('/question/create', CreateQuestion)
    ,('login', homepage.Login)
], debug=True)































