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
	q_id=ndb.StringProperty()
	q_title=ndb.StringProperty()
	q_content=ndb.TextProperty(indexed=False) #???
	q_tags=ndb.StringProperty(repeated=True) #???
	create_time=ndb.DateTimeProperty(auto_now_add=True)
	edit_time=ndb.DateTimeProperty(auto_now_add=True)
	vd_num=ndb.IntegerProperty()
	vp_num=ndb.IntegerProperty()

	@classmethod
	def get_question_one(cls, quser, qid):
		question=Question.query(ndb.AND(Question.q_user == quser, Question.q_id == qid))
		return question.fetch()

	@classmethod
	def get_questions_all(cls, quser):
		question=Question.query(Question.q_user==quser)
		question.order(Question.create_time)
		return question.fetch()

	@classmethod
	def get_every_question(cls):
		question=Question.query(Question.q_user!='')
		question.order(Question.create_time)
		return question.fetch()

class Vote(ndb.Model):
	up_down=ndb.StringProperty()
	q_id=ndb.StringProperty()
	a_id=ndb.StringProperty()
	v_user=ndb.StringProperty()
	v_time=ndb.DateTimeProperty()	

	@classmethod
	def get_user_vote(cls, user):
		vote=Vote.query(Vote.q_user==user)
		return vote.fetch()

	@classmethod
	def get_user_vote_q(cls, user, qid):
		vote=Vote.query(ndb.AND(Vote.q_user==user, Vote.q_id==qid))
		return vote.fetch()

	@classmethod
	def get_user_vote_a(cls, user, qid, aid):
		vote=Vote.query(ndb.AND(Vote.q_user==user, Vote.q_id==qid, Vote.a_id==aid))
		return vote.fetch()

	@classmethod
	def get_q_vote(cls, qid):
		up_count=0
		down_count=0
		vote=Vote.query(ndb.AND(Vote.q_id==qid, Vote.a_id==None))
		for v in vote.fetch():
			if str(v.vote) == "Up":
				up_count+=1
			else:
				down_count+=1
		return (up_count, down_count)

	@classmethod
	def get_a_vote(cls, qid, aid):
		up_count=0
		down_count=0
		vote=Vote.query(ndb.AND(Vote.q_id==qid, Vote.a_id==aid))
		for v in vote.fetch():
			if str(v.vote) == "Up":
				up_count+=1
			else:
				down_count+=1
		return (up_count, down_count)








