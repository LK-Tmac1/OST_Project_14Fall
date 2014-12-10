from google.appengine.ext import ndb

####Image
class Image(ndb.Model):
	img_user=ndb.StringProperty()
	img_url=ndb.StringProperty()
	img_file = ndb.BlobProperty()
	created_date=ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_img_all(cls, user):
		target_img=Image.query(Image.img_user == user)
		target_img.order(-Image.date)
		return target_img.fetch()

	@classmethod
	def get_img_one(cls, user, url):
		target_img=Image.query(ndb.AND(Image.img_user == user, Image.img_url=url))
		target_img.order(-Image.date)
		return target_img.fetch()

####Question
class Question(nbd.Model):
	author=ndb.StringProperty()
	qname=ndb.StringProperty()
	qid=ndb.StringProperty()
	content=ndb.TextProperty(indexed=False) #???
	created_date=ndb.DateTimeProperty(auto_now_add=True)
	edited_date=ndb.DateTimeProperty(auto_now_add=True)
	questiontags=ndb.StringProperty(repeated=True) #???

	@classmethod
	def get_question_one(cls, author,qid):
		question=Question.query(ndb.AND(Question.author == author, Question.qid == qid))
		return question

	@classmethod
	def get_questions_all(cls, author):
		question=Question.query(Question.author=author)
		question.order(-Question.created_date)
		question.order(-Question.qname)
		return question.fetch()

	@classmethod
	def 










