import os
import urllib
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('html'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

TITLE_HOME="NYU Quora"
TITLE_CREATE_Q="Ask NYU"
USER_MODE=0
ADMIN_MODE=1
GUEST_MODE=2
LEFT_NAV_USER_TEMP='left_nav_user.html'
LEFT_NAV_GUEST_TEMP='left_nav_guest.html'
LEFT_NAV_ADMIN_TEMP='left_admin_user.html'
INCORRECT_BEHAVIOR_TEMP='incorrect_behavior.html'
HEADER_TEMP='header.html'
FOOTER_TEMP='footer.html'
CREATE_Q_TEMP='create_question.html'
VIEW_Q_HEADER_TEMP='view_question_header.html'
VIEW_Q_LIST_TEMP='view_question_list.html'

EMPTY_Q_CONTENT_MESSAGE="The content of the question should not be empty!"


def header(self, title=""):
    self.response.write(JINJA_ENVIRONMENT.get_template(HEADER_TEMP).render({"title":title}))

def footer(self):
    self.response.write(JINJA_ENVIRONMENT.get_template(FOOTER_TEMP).render())

def invalid_behavior(self, message="Invalid behavior"):
	self.response.write(JINJA_ENVIRONMENT.get_template(INCORRECT_BEHAVIOR_TEMP).render({"message":message}))

def check_string_empty(content):
	return not content or content == "" or content.isspace()

def left_nav(self, mode=GUEST_MODE, templ_para={}):
	if mode == USER_MODE:
		self.response.write(JINJA_ENVIRONMENT.get_template(LEFT_NAV_USER_TEMP).render(templ_para))
	elif mode == GUEST_MODE:
		self.response.write(JINJA_ENVIRONMENT.get_template(LEFT_NAV_GUEST_TEMP).render(templ_para))
	elif mode == ADMIN_MODE:
		self.response.write(JINJA_ENVIRONMENT.get_template(LEFT_NAV_ADMIN_TEMP).render(templ_para))

def view_question_header(self):
    self.response.write(JINJA_ENVIRONMENT.get_template(VIEW_Q_HEADER_TEMP).render())

def view_question_list(self):
    self.response.write(JINJA_ENVIRONMENT.get_template(VIEW_Q_LIST_TEMP).render())




