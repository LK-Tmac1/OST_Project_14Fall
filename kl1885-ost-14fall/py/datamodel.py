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
		target_img=Image.query(ndb.AND(Image.img_user == user, Image.img_url==url))
		target_img.order(-Image.date)
		return target_img.fetch()

####Question
class Question(ndb.Model):
	q_user=ndb.StringProperty()
	q_name=ndb.StringProperty()
	q_id=ndb.StringProperty()
	q_content=ndb.TextProperty(indexed=False) #???
	q_tags=ndb.StringProperty() #???
	create_date=ndb.DateTimeProperty(auto_now_add=True)
	edit_date=ndb.DateTimeProperty(auto_now_add=True)
	vd_num=ndb.IntegerProperty()
	vp_num=ndb.IntegerProperty()

	@classmethod
	def get_question_one(cls, q_user,qid):
		question=Question.query(ndb.AND(Question.q_user == q_user, Question.qid == qid))
		return question

	@classmethod
	def get_questions_all(cls, q_user):
		question=Question.query(Question.q_user==q_user)
		question.order(-Question.created_date)
		question.order(-Question.qname)
		return question.fetch()










