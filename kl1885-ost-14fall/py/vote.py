import webapp2, datetime, time, py.homepage as homepage, py.jinjaprint as jinjaprint, py.utility as utility
from py.datamodel import *
from google.appengine.api import users
from google.appengine.ext import ndb


def vote(self):
    v_user=str(users.get_current_user())
    qid=str(self.request.get("qid"))
    aid=str(self.request.get("aid"))
    vote=None
    jinjaprint.header(self,jinjaprint.TITLE_VOTE)
    jinjaprint.left_nav(self)
    if not v_user:
        jinjaprint.return_message(self, jinjaprint.MESSAGE_LOGIN_FIRST)
    else:
        mode=""
        if aid:
            vote=Vote().get_user_vote_a(v_user,aid)
        else:
            vote=Vote().get_user_vote_q(v_user,qid)
        if not vote:
            vote=Vote()
        else:
            vote=vote[0]
        up_down=self.request.get("vote")
        v_time=datetime.datetime.now().replace(microsecond=0)
        vote.v_user=v_user
        if aid:
            vote.a_id=aid
            vote.q_id=None
            mode="answer"
        else:
            vote.q_id=qid
            vote.a_id=None
            mode="question"
        vote.up_down=up_down
        vote.v_time=v_time
        vote.put()
        templ_para={'link': jinjaprint.URL_VOTE+"?user="+v_user+"&listmode="+mode}
        message=jinjaprint.MESSAGE_VOTE_SUCCEED+mode+"."
        jinjaprint.return_message(self, message, templ_para)

    jinjaprint.content_end(self)
    jinjaprint.footer(self)

class ListVote(webapp2.RequestHandler):
    def get(self):
        current_user=str(users.get_current_user())
        v_user=str(self.request.get("list"))
        listmode=str(self.request.get("list"))
        jinjaprint.header(self,jinjaprint.TITLE_HOME)
        jinjaprint.left_nav(self)
        jinjaprint.view_top_link(self)
        votelist=None

        if v_user:
            if listmode:
                if listmode.lower()=="question":
                    if current_user == v_user:
                        jinjaprint.view_header(self, jinjaprint.HEADER_LIST_MY_V_Q)
                    else:
                        jinjaprint.view_header(self, jinjaprint.HEADER_LIST_OTHER_V_Q+v_user)
                    votelist=Vote.get_user_vote_all_q(v_user)
                elif listmode.lower()=="answer":
                    votelist=Vote.get_user_vote_all_a(v_user)
                    if current_user == v_user:
                        jinjaprint.view_header(self, jinjaprint.HEADER_LIST_MY_V_A)
                    else:
                        jinjaprint.view_header(self, jinjaprint.HEADER_LIST_OTHER_V_Q+v_user)
                    jinjaprint.view_header(self, jinjaprint.HEADER_LIST_MY_V_Q)
                else:
                    jinjaprint.return_message(jinjaprint.MESSAGE_INVALID_PARA_VOTE)
            else:
                votelist=Vote.get_user_all_vote(v_user)
                if current_user == v_user:
                    jinjaprint.view_header(self, jinjaprint.HEADER_LIST_MY_ALL_V)
                else:
                    jinjaprint.view_header(self, jinjaprint.HEADER_LIST_OTHER_ALL_V+v_user)
        elif listmode:
            if listmode.lower()=="question":
                votelist=Vote.get_q_all_vote(v_user)
                jinjaprint.view_header(self, jinjaprint.HEADER_LIST_MY_V_A)
            elif listmode.lower()=="answer":
                votelist=Vote.get_a_all_vote(v_user)
            else:
                jinjaprint.return_message(jinjaprint.MESSAGE_INVALID_PARA_VOTE)
        else:
            votelist=Vote.get_all_vote()
            jinjaprint.view_header(self, jinjaprint.HEADER_LIST_ALL_VOTE)

        for vote in votelist:
            aid = vote.a_id
            qid = vote.q_id
            templ_para={}
            a=None
            q=None
            if aid:
                a = Answer.get_by_aid(aid)[0]
            elif qid:
                q = Question.get_by_qid(qid)[0]
            templ_para={'a':a, 'q':q, 'v':vote, 'current_user':current_user}
            jinjaprint.list_vote(self, templ_para)

        jinjaprint.content_end(self)
        jinjaprint.footer(self)


    def post(self):
        vote(self)

app = webapp2.WSGIApplication([
     (jinjaprint.URL_VOTE, ListVote)
], debug=True)