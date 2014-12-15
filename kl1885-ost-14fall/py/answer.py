import webapp2, datetime, time, py.homepage as homepage, py.jinjaprint as jinjaprint, py.utility as utility
from py.datamodel import *
from google.appengine.api import users
from google.appengine.ext import ndb

def put_answer(self, add_new):
	current_user=users.get_current_user()
	qid=str(self.request.get('qid'))
	qtitle=unicode(self.request.get('qtitle'))
	submit=self.request.get("submit")
	if submit.lower()=="cancel":
		self.redirect(jinjaprint.URL_VIEW_Q+"?qid="+qid)
	elif submit.lower() == "submit":
		a_content=unicode(self.request.get("acontent"))
		jinjaprint.header(self,jinjaprint.TITLE_ADD_A)
		jinjaprint.left_nav(self)

		if utility.check_string_empty(a_content):
			jinjaprint.return_message(self, jinjaprint.MESSAGE_EMPTY_A_CONTENT)
		else:
			if add_new:
				newA=Answer()
				newA.a_user=str(current_user)
				newA.q_id=str(qid)
				create_time=datetime.datetime.now()
				newA.create_time=create_time.replace(microsecond=0)
				newA.edit_time=create_time.replace(microsecond=0)
				newA.a_id=create_time.strftime("%s")
				newA.a_content=a_content
				newA.vd_num=0
				newA.vp_num=0
				newA.put()
				templ_para={'link': jinjaprint.URL_VIEW_Q+"?qid="+str(qid)}
				message=utility.replace_newline(jinjaprint.MESSAGE_SUCCEED_NEW_A+"\n\n\n"+qtitle)
				jinjaprint.return_message(self, message, templ_para)
			else:
				aid=str(self.request.get("aid"))
				editA=Answer.get_by_aid(aid)[0]
				if editA.a_user != str(current_user):
					jinjaprint.return_message(self, jinjaprint.MESSAGE_CANNOT_EDIT_A)
				else:
					editA.a_content=unicode(self.request.get("acontent"))
					editA.edit_time=datetime.datetime.now().replace(microsecond=0)
					editA.put()
					templ_para={'link': jinjaprint.URL_VIEW_Q+"?qid="+editA.q_id}
					message=utility.replace_newline(jinjaprint.MESSAGE_SUCCEED_EDIT_A)
					jinjaprint.return_message(self, message, templ_para)

        jinjaprint.footer(self)


class AddAnswer(webapp2.RequestHandler):
	def get(self):
		current_user = users.get_current_user()		
		jinjaprint.header(self, jinjaprint.TITLE_ADD_A)
		jinjaprint.left_nav(self)
		jinjaprint.view_top_link(self)
		jinjaprint.view_header(self, jinjaprint.HEADER_ADD_A)

		if not current_user:
			jinjaprint.return_message(self, jinjaprint.MESSAGE_LOGIN_FIRST)
		else:
			qid=str(self.request.get("qid"))
			Q=Question.get_by_qid(qid)
			if len(Q) == 0:
				jinjaprint.return_message(self, jinjaprint.MESSAGE_NO_SUCH_QID+qid)
			else:
				q=Q[0]
				q.q_content=utility.replace_content(q.q_content)
				templ_para={'q': q, 'view_question_mode':False}
				jinjaprint.view_full_question(self, templ_para)
				jinjaprint.add_answer(self, templ_para)
		jinjaprint.footer(self)

	def post(self):
		put_answer(self, True)


class EditAnswer(webapp2.RequestHandler):
	def get(self):
		current_user = users.get_current_user()
		jinjaprint.header(self, jinjaprint.TITLE_EDIT_A)
		jinjaprint.left_nav(self)
		jinjaprint.view_top_link(self)
		jinjaprint.view_header(self, jinjaprint.HEADER_EDIT_A)
		aid=str(self.request.get("aid"))
		A=Answer.get_by_aid(aid)
		if not current_user:
			jinjaprint.return_message(self, jinjaprint.MESSAGE_LOGIN_FIRST)
		elif len(A) == 0:
			jinjaprint.return_message(self, jinjaprint.MESSAGE_NO_SUCH_AID+aid)
		elif A[0].a_user != str(current_user):
			jinjaprint.return_message(self, jinjaprint.MESSAGE_CANNOT_EDIT_A)
		else:
			Q=Question.get_by_qid(str(A[0].q_id))
			if len(Q) == 0:
				jinjaprint.return_message(self, jinjaprint.MESSAGE_NO_Q_FOR_AID+aid)
			else:
				a=A[0]
				a.a_content=utility.replace_content(a.a_content)
				templ_para={'a': a, 'q': Q[0]}
				jinjaprint.view_full_question(self, templ_para)
				jinjaprint.edit_answer(self, templ_para)
		
		jinjaprint.footer(self)

	def post(self):
		put_answer(self, False)
		

app = webapp2.WSGIApplication([
     (jinjaprint.URL_ANSWER, AddAnswer)
     ,(jinjaprint.URL_ANSWER_ADD, AddAnswer)
    ,(jinjaprint.URL_ANSWER_EDIT, EditAnswer)
], debug=True)