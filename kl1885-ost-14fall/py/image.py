import os, urllib, webapp2
import datetime, py.jinjaprint as jinjaprint, py.utility as utility
from py.datamodel import *
from google.appengine.api import users
from google.appengine.ext import ndb

class ShowImage(webapp2.RequestHandler):
	def get(self):
		url=str(self.request.url)
		begin = url.find("image/")+len("image/")
		url=url[begin:len(url)]
		print "url", url
		picture = Image.get_img_by_url(url)
		if len(picture) > 0:
			if picture[0].image_file:
				self.response.headers['Content-Type'] = 'image/png'
				self.response.out.write(picture[0].image_file)
		else:
			jinjaprint.header(self, jinjaprint.TITLE_VIEW_IMAGE)
			jinjaprint.left_nav(self)
			jinjaprint.view_header(self, jinjaprint.HEADER_UPLOAD_IMAGE)
			jinjaprint.return_message(self, jinjaprint.MESSAGE_IMAGE_NOT_FOUND+url)
			jinjaprint.content_end(self)
			jinjaprint.footer(self)


class ListImage(webapp2.RequestHandler):
	def get(self):
		jinjaprint.header(self, jinjaprint.TITLE_VIEW_IMAGE)
		jinjaprint.left_nav(self)
		image_user=str(self.request.get('user'))
		current_user = users.get_current_user()

		imageList=None
		if image_user:
			header=""
			if image_user == str(current_user):
				header=" yourself:"
			else:
				header=" user "+image_user+":"
			jinjaprint.view_header(self, jinjaprint.HEADER_LIST_USER_IMAGE+header)
			imageList=Image.get_img_by_user(image_user)
		else:
			jinjaprint.view_header(self, jinjaprint.HEADER_LIST_ALL_IMAGE)
			imageList=Image.get_img_all()

		if imageList:
			temp_para={"imageList":imageList, "currentuser":current_user}
			jinjaprint.list_image(self, temp_para)
		else:
			jinjaprint.return_message(self, jinjaprint.MESSAGE_IMAGE_NOT_FOUND)

		jinjaprint.content_end(self)
		jinjaprint.footer(self)

	def post(self):
		image_url=str(self.request.get("image_url"))
		current_user=users.get_current_user()
		jinjaprint.header(self, jinjaprint.TITLE_VIEW_IMAGE)
		jinjaprint.left_nav(self)

		if not current_user:
			jinjaprint.return_message(self, jinjaprint.MESSAGE_LOGIN_FIRST)
		else:
			image=Image.get_img_by_url(image_url)
			if len(image) > 0:
				image=image[0]
				if str(current_user) == image.image_user:
					image.key.delete()
					jinjaprint.return_message(self, jinjaprint.MESSAGE_SUCCESS_DELETE_IMAGE)
				else:
					jinjaprint.return_message(self, jinjaprint.MESSAGE_NO_RIGHT_DELETE_IMAGE)
			else:
				jinjaprint.return_message(self, jinjaprint.MESSAGE_IMAGE_NOT_FOUND+image_url)
		
		jinjaprint.content_end(self)
		jinjaprint.footer(self)


class UploadImage(webapp2.RequestHandler):
	
	def get(self):
		current_user=users.get_current_user()
		if not current_user:
			self.redirect(jinjaprint.URL_QUESTION)
		else:
			jinjaprint.header(self, jinjaprint.TITLE_UPLOAD_IMAGE)
			jinjaprint.left_nav(self)
			jinjaprint.view_header(self, jinjaprint.HEADER_UPLOAD_IMAGE)
			jinjaprint.upload_image(self)
			jinjaprint.content_end(self)
			jinjaprint.footer(self)
	
	def post(self):
		current_user=users.get_current_user()
		if not current_user:
			self.redirect(jinjaprint.URL_QUESTION)
		else:
			image=Image()
			image.image_file=self.request.get("img")
			image.filename=str(self.request.params['img'].filename).strip()
			image.upload_time=datetime.datetime.now().replace(microsecond=0)
			image.image_user=str(current_user)
			image_key=image.put()
			image = Image.get_by_id(image_key.id())
			image.image_url = str(image_key.id())+"_"+image.filename
			image.put()
			jinjaprint.header(self, jinjaprint.TITLE_UPLOAD_IMAGE)
			jinjaprint.left_nav(self)
			temp_para={'link':image.image_url}
			jinjaprint.return_message(self, jinjaprint.MESSAGE_IMG_UPLOADED, temp_para)
			jinjaprint.content_end(self)
			jinjaprint.footer(self)


app = webapp2.WSGIApplication([
    (jinjaprint.URL_IMAGE_LIST, ListImage ),
    (jinjaprint.URL_IMAGE_UPLOAD, UploadImage),
    (jinjaprint.URL_IMAGE+"/.*", ShowImage)
], debug=True)
