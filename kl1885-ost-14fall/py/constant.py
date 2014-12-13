import os, urllib, datetime, jinja2, time, py.datamodel as model
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader('html'),
	extensions=['jinja2.ext.autoescape'], autoescape=True)

URL_MY_Q='/myquestion'
URL_HOME='/homepage'
URL_LOGIN='/login'
URL_LOGOUT='/logout'
URL_CREATE_Q='/question/create'
URL_VIEW_Q='/question/view'
URL_EDIT_Q='/question/edit'

TITLE_VIEW_Q="View Question"
TITLE_HOME="NYU Quora"
TITLE_CREATE_Q="Ask NYU"
TITLE_MY_Q="My Question"
TITLE_SUCCESS='Succeed!'
TITLE_ERROR='Oops...'
HTML_CURRENT_USER='current_user'
HTML_LOGOUT_URL='logout_url'
HTML_LOGIN_URL='login_url'
HTML_Q_LOOP='Qs'
HTML_SINGLE_Q='q'
HTML_Q_TAGS='qtags'
HTML_VIEW_MY_Q="view_my_question"
HTML_TAG_Q="question_tag"

MODE_USER=0
MODE_ADMIN=1
MODE_GUEST=2
MODE_VIEW_ALL_Q='View all existed questions:'
MODE_VIEW_Q='More details about this question:'
MODE_VIEW_MY_Q='I asked:'
MODE_ADD_Q='question'
MODE_ADD_A='answer'
MODE_ADD_I='image'
MODE_TAG_MY_Q='myquestion'
MODE_TAG_ALL_Q='question'

TEMP_LEFT_NAV_USER='left_nav_user.html'
TEMP_LEFT_NAV_GUEST='left_nav_guest.html'
TEMP_LEFT_NAV_ADMIN='left_admin_user.html'
TEMP_SIMPLE_MESSAGE='simple_message.html'
TEMP_HEADER='header.html'
TEMP_FOOTER='footer.html'
TEMP_CREATE_Q='create_question.html'
TEMP_EDIT_Q='edit_question.html'
TEMP_VIEW_Q_HEADER='view_question_header.html'
TEMP_VIEW_Q_LIST='view_question_list.html'
TEMP_VIEW_Q='view_question.html'
MESSAGE_EMPTY_Q_TITLE="Don't be too lazy to give it a title, please..."
MESSAGE_EMPTY_Q_CONTENT="Oh please... ask some real stuff, OK?"
MESSAGE_NO_SUCH_QID="Sorry, no such a question: "
MESSAGE_SUCCEED_NEW_Q="New question added! Now direct to the previous page..."
MESSAGE_CANNOT_EDIT_Q="Oh please, this question doesn't belong to you..."
DEFAULT_Q_ID='0000000000'
DEFAULT_Q_TITLE='default_question_title'

def header(self, title=""):
    self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_HEADER).render({"title":title}))

def footer(self):
    self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_FOOTER).render())

def simple_message(self, title, message,redirectURL=None):
	templ_val={
	"title": title
	,"message": message
	}
	self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_SIMPLE_MESSAGE).render(templ_val))
	footer(self)
	#time.sleep(2)
	#if redirectURL != None:
	#	self.redirect(redirectURL)


def show_error(self, message):
	simple_message(self, TITLE_ERROR, message)

def check_string_empty(content):
	return not content or content == "" or content.isspace()

def left_nav(self, mode=MODE_GUEST, templ_para={}):
	if mode == MODE_USER:
		self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_LEFT_NAV_USER).render(templ_para))
	elif mode == MODE_GUEST:
		self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_LEFT_NAV_GUEST).render(templ_para))
	elif mode == MODE_ADMIN:
		self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_LEFT_NAV_ADMIN).render(templ_para))

def view_question_header(self,view_mode):
    self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_VIEW_Q_HEADER).render({HTML_VIEW_MY_Q:view_mode}))

def view_question_list(self,templ_para):
    self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_VIEW_Q_LIST).render(templ_para))

def view_question(self, templ_para):
    self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_VIEW_Q).render(templ_para))

def create_question_form(self):
	self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_CREATE_Q).render())

def login(self):
	self.redirect(users.create_login_url(self.request.uri))

def logout(self):
	self.redirect(users.create_logout_url(self.request.uri))

def tag_split(tags, delimit=','):
	if check_string_empty(tags):
		return tags.split(delimit)
	else:
		return []

def vote_q(self):
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

def show_success(self,redirectURL=None):
	simple_message(self, TITLE_SUCCESS, MESSAGE_SUCCEED_NEW_Q, redirectURL)

def split_tags(tag_string):
	tag_list = tag_string.split(',')
  	for x in xrange(len(tag_list)):
  		tag_list[x] = tag_list[x].strip()
		if tag_list[x] == '':
			tag_list[x] = None
	  	tag_list = filter(None, tag_list)
	  	tag_list = list(set(tag_list))
  	return tag_list

