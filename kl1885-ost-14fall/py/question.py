import webapp2
import datetime
import time
import py.homepage as homepage
import py.constant as constant
from py.datamodel import *

from google.appengine.api import users
from google.appengine.ext import ndb


class CreateQuestion(webapp2.RequestHandler):
    def get(self):
        constant.header(self,constant.TITLE_CREATE_Q)
        current_user = users.get_current_user()
        if not current_user:
            constant.login(self)
        else:
            templ_value={
            constant.HTML_CURRENT_USER: unicode(current_user)
            ,constant.HTML_LOGOUT_URL: users.create_logout_url(self.request.uri)
            }
            constant.left_nav(self, constant.MODE_USER, templ_value)
            constant.create_question_form(self)

        constant.footer(self)

    def post(self):
        current_user = users.get_current_user()
        submit=self.request.get("submit")
        if not current_user:
            constant.login(self)
        elif submit == "Cancel":
            self.redirect(constant.URL_HOME)
        elif submit == "Submit":
            q_content=unicode(self.request.get("qcontent"))
            q_title=unicode(self.request.get("qtitle"))
            if constant.check_string_empty(q_title):
                constant.show_error(self, constant.MESSAGE_EMPTY_Q_TITLE)
            elif constant.check_string_empty(q_content):
                constant.show_error(self, constant.MESSAGE_EMPTY_Q_CONTENT)
            else:
                newQ=Question()
                newQ.q_user=unicode(current_user)
                newQ.q_content=q_content
                tag_string=unicode(self.request.get("qtags"))
                newQ.q_tags=constant.split_tags(tag_string)
                if not self.request.get("qtitle").isspace():
                    newQ.q_title=unicode(self.request.get("qtitle"))
                else:
                    newQ.q_title=constant.DEFAULT_Q_TITLE
                create_time=datetime.datetime.now()
                newQ.create_time=create_time.replace(microsecond=0)
                newQ.edit_time=create_time.replace(microsecond=0)
                newQ.q_id=create_time.strftime("%s")
                newQ.vd_num=0
                newQ.vp_num=0
                a=newQ.put()
                constant.show_success(self,constant.URL_MY_Q)

class EditQuestion(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        qid=self.request.get("qid")
        quser=self.request.get("quser")
        Q=Question.get_question_one(str(quser), str(qid))
        if len(Q) == 0:
            constant.show_error(self, constant.MESSAGE_NO_SUCH_QID+str(qid))
        elif str(quser) != str(current_user):
            constant.show_error(self, constant.MESSAGE_CANNOT_EDIT_Q)
        else:
            print ""



class ViewQuestion(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        qid=self.request.get("qid")
        quser=self.request.get("quser")
        Q=Question.get_question_one(str(quser), str(qid))
        if len(Q) == 0:
            constant.show_error(self, constant.MESSAGE_NO_SUCH_QID+str(qid))
        else:
            constant.header(self, constant.TITLE_VIEW_Q)
            q=Q[0]
            quser=q.q_user
            qid=q.q_id
            #As = Answer.get_all_answer_by_qid()
            if current_user:
                templ_value={
                 constant.HTML_CURRENT_USER: unicode(current_user)
                ,constant.HTML_LOGOUT_URL: users.create_logout_url(self.request.uri)
                ,constant.HTML_SINGLE_Q: Q[0]
                ,constant.HTML_TAG_Q: constant.MODE_TAG_ALL_Q
                }
                constant.left_nav(self, constant.MODE_USER, templ_value)
                constant.view_question_header(self,constant.MODE_VIEW_Q)
                constant.view_question(self, templ_value)
            else:
                templ_value={
                constant.HTML_LOGIN_URL: users.create_logout_url(self.request.uri)
                }
                constant.left_nav(self, constant.MODE_USER, templ_value)


            constant.footer(self)




class MyQuestion(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        if not current_user:
            constant.login(self)
        else:
            Qs=Question.get_questions_all(unicode(current_user))
            templ_value={
            constant.HTML_CURRENT_USER: unicode(current_user)
            ,constant.HTML_LOGOUT_URL: users.create_logout_url(self.request.uri)
            ,constant.HTML_Q_LOOP: Qs
            ,constant.HTML_VIEW_MY_Q: True
            ,constant.HTML_TAG_Q: constant.MODE_TAG_MY_Q
            }
            constant.header(self, constant.TITLE_MY_Q)
            constant.left_nav(self, constant.MODE_USER, templ_value)
            constant.view_question_header(self, constant.MODE_VIEW_MY_Q)
            constant.view_question_list(self, templ_value)
        
        constant.footer(self)




app = webapp2.WSGIApplication([
     (constant.URL_CREATE_Q, CreateQuestion)
    ,(constant.URL_MY_Q, MyQuestion)
    ,(constant.URL_VIEW_Q, ViewQuestion)
    ,(constant.URL_EDIT_Q, EditQuestion)
], debug=True)































