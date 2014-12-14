import webapp2, datetime, time, py.homepage as homepage, py.jinjaprint as jinjaprint, py.utility as utility
from py.datamodel import *
from google.appengine.api import users
from google.appengine.ext import ndb

def show_question(self, mode_all):
    page_num = self.request.get('page')
    tag=str(self.request.get('tag'))
    current_user = users.get_current_user()
    templ_para={"current_user":unicode(current_user)}
    max_page_num=0
    jinjaprint.header(self,jinjaprint.TITLE_HOME)
    jinjaprint.left_nav(self)
    jinjaprint.view_top_link(self)
    Qs=[]
    if mode_all:
        templ_para['view_my_question']=False
        templ_para['tag_mode']= jinjaprint.MODE_TAG_ALL_Q
        if tag:
            Qs=Question.get_by_tag(tag)
            jinjaprint.view_header(self, jinjaprint.HEADER_VIEW_TAG_Q_ALL+tag)
        else:
            Qs=Question.get_all()
            jinjaprint.view_header(self, jinjaprint.HEADER_VIEW_ALL_Q)
    else:
        templ_para['view_my_question']=True
        templ_para['tag_mode']= jinjaprint.MODE_TAG_MY_Q
        if tag:
            Qs=Question.get_by_tag_user(tag,str(current_user))
            jinjaprint.view_header(self, jinjaprint.HEADER_VIEW_TAG_Q_ALL+tag)
        else:
            Qs=Question.get_by_user_all(unicode(current_user))
            jinjaprint.view_header(self, jinjaprint.HEADER_VIEW_MY_Q)

    if page_num and not str(page_num).isdigit():
        jinjaprint.simple_message(self, jinjaprint.MESSAGE_INVALID_PAGE_NUM)
    else:
        num_of_q = len(Qs)
        if not str(page_num):
            page_num=1
        else:
            page_num=int(page_num)
            max_page_num=utility.max_page_num(len(Qs))
        Qs=utility.split_element_by_page_num(Qs,page_num)
        if len(Qs) != 0:
            jinjaprint.page_num_temp(self, max_page_num, current_page=page_num)
        templ_para['Qs']=Qs
        jinjaprint.show_question_list(self, templ_para)
        if len(Qs) != 0:
            jinjaprint.page_num_temp(self, max_page_num, current_page=page_num)
        jinjaprint.footer(self)

class CreateQuestion(webapp2.RequestHandler):
    def get(self):
        jinjaprint.header(self,jinjaprint.TITLE_CREATE_Q)
        jinjaprint.left_nav(self)
        current_user = users.get_current_user()
        if not current_user:
            jinjaprint.simple_message(self, jinjaprint.MESSAGE_LOGIN_FIRST)
        else:
            jinjaprint.create_question(self)

        jinjaprint.footer(self)

    def post(self):
        current_user = users.get_current_user()
        submit=self.request.get("submit")
        if submit == "Cancel":
            self.redirect(jinjaprint.URL_QUESTION)
        elif submit == "Submit":
            q_content=unicode(self.request.get("qcontent"))
            q_title=unicode(self.request.get("qtitle"))
            jinjaprint.header(self,jinjaprint.TITLE_CREATE_Q)
            jinjaprint.left_nav(self)

            if utility.check_string_empty(q_title):
                jinjaprint.simple_message(self, jinjaprint.MESSAGE_EMPTY_Q_TITLE)
            elif utility.check_string_empty(q_content):
                jinjaprint.simple_message(self, jinjaprint.MESSAGE_EMPTY_Q_CONTENT)
            else:
                newQ=Question()
                newQ.q_user=unicode(current_user)
                newQ.q_content=q_content
                tag_string=unicode(self.request.get("qtags"))
                newQ.q_tags=utility.tag_split(tag_string)
                newQ.q_title=unicode(self.request.get("qtitle"))
                create_time=datetime.datetime.now()
                newQ.create_time=create_time.replace(microsecond=0)
                newQ.edit_time=create_time.replace(microsecond=0)
                newQ.q_id=create_time.strftime("%s")
                newQ.vd_num=0
                newQ.vp_num=0
                a=newQ.put()
                jinjaprint.simple_message(self,jinjaprint.MESSAGE_SUCCEED_NEW_Q)

        jinjaprint.footer(self)

class EditQuestion(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        if not current_user:
            jinjaprint.login(self)
        qid=self.request.get("qid")
        quser=self.request.get("quser")
        Q=Question.get_by_user_one(str(quser), str(qid))
        if not quser:
            jinjaprint.show_error(self, jinjaprint.MESSAGE_NO_Q_USER+str(qid))
        elif len(Q) == 0:
            jinjaprint.show_error(self, jinjaprint.MESSAGE_NO_SUCH_QID+str(qid))
        elif str(quser) != str(current_user):
            jinjaprint.show_error(self, jinjaprint.MESSAGE_CANNOT_EDIT_Q)
        else:
            jinjaprint.header(self,jinjaprint.TITLE_EDIT_Q)
            jinjaprint.left_nav(self)
            tag_string=utility.merge_tags(Q[0].q_tags)
            templ_para={
            'q':Q[0]
            ,'qtags': tag_string
            }
            jinjaprint.edit_question(self, templ_para)
            jinjaprint.footer(self)

    def post(self):
        current_user = users.get_current_user()
        submit=self.request.get("submit")
        if not current_user:
            jinjaprint.login(self)
        elif submit == "Cancel":
            self.redirect(jinjaprint.URL_HOME)
        elif submit == "Submit":
            q_content=unicode(self.request.get("qcontent"))
            q_title=unicode(self.request.get("qtitle"))
            if jinjaprint.check_string_empty(q_title):
                jinjaprint.show_error(self, jinjaprint.MESSAGE_EMPTY_Q_TITLE)
            elif jinjaprint.check_string_empty(q_content):
                jinjaprint.show_error(self, jinjaprint.MESSAGE_EMPTY_Q_CONTENT)
            else:
                editQ=Question()
                editQ.q_content=q_content
                editQ.q_user=unicode(current_user)
                tag_string=unicode(self.request.get("qtags"))
                editQ.q_tags=jinjaprint.split_tags(tag_string)
                editQ.q_title=unicode(self.request.get("qtitle"))
                editQ.edit_time=datetime.datetime.now().replace(microsecond=0)
                editQ.put()
                jinjaprint.show_success(self,jinjaprint.URL_MY_Q)


class ViewFullQuestion(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        jinjaprint.header(self, jinjaprint.TITLE_VIEW_Q)
        jinjaprint.left_nav(self)
        jinjaprint.view_top_link(self)
        jinjaprint.view_header(self, jinjaprint.HEADER_VIEW_Q)

        qid=self.request.get("qid")
        Q=Question.get_by_qid(str(qid))
        if len(Q) > 0:
            q=Q[0]
            qid=q.q_id
        else:
            q=None
        #As = Answer.get_all_answer_by_qid()
        templ_para={
            'q': q
            ,'view_my_question': jinjaprint.URL_QUESTION
            ,'tag_mode': jinjaprint.MODE_TAG_ALL_Q
        }
        jinjaprint.view_full_question(self, templ_para)
        jinjaprint.footer(self)


class ListAllQuestion(webapp2.RequestHandler):
    def get(self):
        show_question(self, True)


class ListMyQuestion(webapp2.RequestHandler):
    def get(self):
        show_question(self, False)


app = webapp2.WSGIApplication([
     (jinjaprint.URL_QUESTION, ListAllQuestion)
     ,(jinjaprint.URL_SHOW_ALL_Q, ListAllQuestion)
    ,(jinjaprint.URL_SHOW_MY_Q, ListMyQuestion)
    ,(jinjaprint.URL_CREATE_Q, CreateQuestion)
    ,(jinjaprint.URL_VIEW_Q, ViewFullQuestion)
    ,(jinjaprint.URL_EDIT_Q, EditQuestion)
], debug=True)