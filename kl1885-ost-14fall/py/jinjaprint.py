import os, urllib, jinja2, py.utility as utility
from google.appengine.api import users

URL_HOME='/homepage'
URL_LOGIN='/login'
URL_LOGOUT='/logout'
URL_QUESTION='/question'
URL_SHOW_ALL_Q=URL_QUESTION+'/all'
URL_SHOW_MY_Q=URL_QUESTION+'/mine'
URL_CREATE_Q=URL_QUESTION+'/create'
URL_VIEW_Q=URL_QUESTION+'/view'
URL_EDIT_Q=URL_QUESTION+'/edit'
URL_TAG_Q=URL_QUESTION+'/tag'
TITLE_VIEW_Q="View Question"
TITLE_HOME="NYU Quora"
TITLE_CREATE_Q="Ask a question"
TITLE_EDIT_Q="Edit question"
TITLE_MY_Q="My Question"
TITLE_TAG_Q='Tag question'
MODE_TAG_MY_Q='mine'
MODE_TAG_ALL_Q='all'
HEADER_VIEW_ALL_Q='View all existed questions: '
HEADER_VIEW_Q='View the full question: '
HEADER_VIEW_MY_Q='View my questions: '
HEADER_VIEW_TAG_Q_ALL="All questions with tag: "
HEADER_VIEW_TAG_Q_MINE="My Questions that with tag: "
TEMP_LEFT_NAV='left_nav.html'
TEMP_HEADER='header.html'
TEMP_FOOTER='footer.html'
TEMP_CREATE_Q='create_question.html'
TEMP_EDIT_Q='edit_question.html'
TEMP_VIEW_TOP_LINK='view_top_link.html'
TEMP_VIEW_HEADER='view_header.html'
TEMP_VIEW_Q_LIST='show_question_list.html'
TEMP_VIEW_Q='view_full_question.html'
TEMP_PAGE_NUM='page_num.html'
TEMP_PUT_MESSAGE='simple_message.html'
MESSAGE_WELCOME_BACK="Welcome back, "
MESSAGE_HELLO_GUEST="Hello you, guest"
MESSAGE_EMPTY_Q_TITLE="Don't be too lazy to give it a title, please..."
MESSAGE_EMPTY_Q_CONTENT="Oh please... ask some real stuff, OK?"
MESSAGE_NO_SUCH_QID="Sorry, no such a question: "
MESSAGE_SUCCEED_NEW_Q="New question added! You can go back My Question to view it."
MESSAGE_SUCCEED_EDIT_Q="Question modified! You can go back My Question to view it."
MESSAGE_CANNOT_EDIT_Q="Oh please, this question doesn't belong to you..."
MESSAGE_NO_SUCH_Q_TAG="Sorry, no question for this tag: "
MESSAGE_INVALID_PAGE_NUM="Invalid page number."
MESSAGE_DUPLICATED_QID="Invalid questions cause duplicated with id: "
MESSAGE_LOGIN_FIRST="You are now a guest so please login first."

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader('html'),
	extensions=['jinja2.ext.autoescape'], autoescape=True)

def header(self, title):
	templ_para={"title":title}
	self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_HEADER).render(templ_para))

def footer(self):
    self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_FOOTER).render())

def view_top_link(self):
    self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_VIEW_TOP_LINK).render())

def page_num_temp(self, page_num, current_page):
	result=utility.get_previous_next_page(page_num, current_page)
	previous=result[0]
	next=result[1]
	templ_para={'num_of_page' : page_num+1,'previous_page': previous,'next_page': next}
	self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_PAGE_NUM).render(templ_para))

def simple_message(self, message):
	templ_para={'message':message}
	self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_PUT_MESSAGE).render(templ_para))

def left_nav(self, admin=False):
	currentuser=users.get_current_user()
	login_out_url=""
	if not currentuser:
		login_out_url=users.create_login_url(self.request.uri)
	else:
		login_out_url=users.create_logout_url(self.request.uri)
	templ_para={'current_user': currentuser, 'login_out_url':login_out_url}
	self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_LEFT_NAV).render(templ_para))

def view_header(self, header):
	templ_para={'view_header': header}
	self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_VIEW_HEADER).render(templ_para))

def show_question_list(self, templ_para):
    self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_VIEW_Q_LIST).render(templ_para))

def view_full_question(self, templ_para):
    self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_VIEW_Q).render(templ_para))

def create_question(self):
	self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_CREATE_Q).render())

def edit_question(self, q_para):
	self.response.write(JINJA_ENVIRONMENT.get_template(TEMP_EDIT_Q).render(q_para))
