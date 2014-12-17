import webapp2, datetime, py.jinjaprint as jinjaprint
from py.datamodel import *
from google.appengine.api import users
from google.appengine.ext import ndb


class RSSGenerator(webapp2.RequestHandler):

	def get(self):
		qid=str(self.request.get('qid'))
		current_user=users.get_current_user()
		if not current_user:
			jinjaprint.header(self, jinjaprint.TITLE_RSS)
			jinjaprint.left_nav(self)
			jinjaprint.return_message(self, jinjaprint.MESSAGE_LOGIN_FIRST)
			jinjaprint.content_end(self)
			jinjaprint.footer(self)
		else:
			qList=None
			if not qid:
				jinjaprint.header(self, jinjaprint.TITLE_RSS)
				jinjaprint.left_nav(self)
				jinjaprint.return_message(self, jinjaprint.MESSAGE_QID_REQUIRED_RSS)
				jinjaprint.content_end(self)
				jinjaprint.footer(self)
			else:
				qList=Question.get_by_qid(qid)
				if qList:
					q=qList[0]
					As=Answer.get_by_qid(qid)
					temp_para={"q":q, "As":As}
					jinjaprint.rss_generator(self, temp_para)
				else:
					jinjaprint.header(self, jinjaprint.TITLE_RSS)
					jinjaprint.left_nav(self)
					jinjaprint.return_message(self, jinjaprint.MESSAGE_NO_SUCH_QID_RSS+qid)
					jinjaprint.content_end(self)
					jinjaprint.footer(self)


app = webapp2.WSGIApplication([
    (jinjaprint.URL_RSS+".*", RSSGenerator)
], debug=True)