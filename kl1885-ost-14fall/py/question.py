import webapp2, datetime, time, py.homepage as homepage, py.jinjaprint as jinjaprint, py.utility as utility
from py.datamodel import *
from google.appengine.api import users
from google.appengine.ext import ndb

def vote_q(self):######
    v_user=users.get_current_user()
    qid=self.request.get("qid")
    aid=self.request.get("aid")
    up_down=self.request.get("vote")
    v_time=datetime.datetime.now().replace(microsecond=0)
    key=str(v_user)+"_"+str(qid)+"_"+str(aid)
    #newV = model.Vote(key_name=key)
    newV=model.Vote()
    newV.v_user=unicode(v_user)
    newV.q_id=qid
    newV.a_id=aid
    newV.up_down=up_down
    newV.v_time=v_time
    newV.put()

def show_question(self, mode_all):
    page_num = self.request.get('page')
    tag=unicode(self.request.get('tag'))
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
            jinjaprint.view_header(self, jinjaprint.HEADER_VIEW_TAG_Q_MINE+tag)
        else:
            Qs=Question.get_by_user_all(unicode(current_user))
            jinjaprint.view_header(self, jinjaprint.HEADER_VIEW_MY_Q)

    if page_num and not str(page_num).isdigit():
        jinjaprint.simple_message(self, jinjaprint.MESSAGE_INVALID_PAGE_NUM)
    else:
        if not str(page_num):
            page_num=1
        else:
            page_num=int(page_num)

        max_page_num=utility.max_page_num(len(Qs))
        Qs=utility.split_element_by_page_num(Qs,page_num)
        for q in Qs:
            q.q_content=utility.replace_content(q.q_content)
            
        if len(Qs) != 0:
            jinjaprint.page_num_temp(self, max_page_num, current_page=page_num)
        templ_para['Qs']=Qs
        jinjaprint.show_question_list(self, templ_para)
        if len(Qs) != 0:
            jinjaprint.page_num_temp(self, max_page_num, current_page=page_num)
        jinjaprint.footer(self)

def put_question(self, createnew):
    current_user = users.get_current_user()
    submit=self.request.get("submit")
    if submit == "Cancel":
        self.redirect(jinjaprint.URL_QUESTION)
    elif submit == "Submit":
        q_content=unicode(self.request.get("qcontent"))
        q_title=unicode(self.request.get("qtitle"))
        tag_string=unicode(self.request.get("qtags"))
        jinjaprint.header(self,jinjaprint.TITLE_CREATE_Q)
        jinjaprint.left_nav(self)

        if utility.check_string_empty(q_title):
            jinjaprint.simple_message(self, jinjaprint.MESSAGE_EMPTY_Q_TITLE)
        elif utility.check_string_empty(q_content):
            jinjaprint.simple_message(self, jinjaprint.MESSAGE_EMPTY_Q_CONTENT)
        else:
            if createnew:
                newQ=Question()
                newQ.q_user=str(current_user)
                newQ.q_content=q_content
                newQ.q_tags=utility.tag_split(tag_string)
                newQ.q_title=q_title
                create_time=datetime.datetime.now()
                newQ.create_time=create_time.replace(microsecond=0)
                newQ.edit_time=create_time.replace(microsecond=0)
                newQ.q_id=create_time.strftime("%s")
                newQ.vd_num=0
                newQ.vp_num=0
                newQ.put()
                jinjaprint.simple_message(self,jinjaprint.MESSAGE_SUCCEED_NEW_Q)
            else:
                qid=self.request.get('qid')
                Qs=Question.get_by_qid(qid)
                if len(Qs) == 0:
                    jinjaprint.simple_message(self,jinjaprint.MESSAGE_NO_SUCH_QID+qid)
                elif len(Qs) > 1:
                    jinjaprint.simple_message(self,jinjaprint.MESSAGE_DUPLICATED_QID+qid)
                else:
                    editQ=Qs[0]
                    editQ.edit_time=datetime.datetime.now().replace(microsecond=0)
                    editQ.q_title=q_title
                    editQ.q_content=q_content
                    editQ.q_tags=utility.tag_split(tag_string)
                    editQ.put()
                    jinjaprint.simple_message(self,jinjaprint.MESSAGE_SUCCEED_EDIT_Q)

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
        put_question(self, True)


class EditQuestion(webapp2.RequestHandler):
    def get(self):
        jinjaprint.header(self,jinjaprint.TITLE_EDIT_Q)
        jinjaprint.left_nav(self)

        current_user = users.get_current_user()
        if not current_user:
            jinjaprint.simple_message(self, jinjaprint.MESSAGE_LOGIN_FIRST)
        else:
            qid=self.request.get("qid")
            Q=Question.get_by_qid(str(qid))

            if len(Q) == 0:
                jinjaprint.simple_message(self, jinjaprint.MESSAGE_NO_SUCH_QID+qid)
            elif str(Q[0].q_user) != str(current_user):
                jinjaprint.simple_message(self, jinjaprint.MESSAGE_CANNOT_EDIT_Q)
            else:
                tag_string=utility.merge_tags(Q[0].q_tags)
                templ_para={'q':Q[0],'qtags': tag_string}
                jinjaprint.edit_question(self, templ_para)
        jinjaprint.footer(self)

    def post(self):
        put_question(self, False)


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

        q.q_content=utility.replace_content(q.q_content)
        templ_para={'q': q, 'tag_mode': jinjaprint.MODE_TAG_ALL_Q, 'current_user':current_user}
        #As = Answer.get_all_answer_by_qid()
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