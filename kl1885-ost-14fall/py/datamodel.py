from google.appengine.ext import ndb

####Image
class Image(ndb.Model):
	img_user=ndb.StringProperty()
	img_url=ndb.StringProperty()
	img_file = ndb.BlobProperty()
	created_date=ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_img_all(cls, user):
		target_img=Image.query(Image.img_user == user).order(-Image.date)
		return target_img.fetch()

	@classmethod
	def get_img_one(cls, user, url):
		target_img=Image.query(ndb.AND(Image.img_user == user, \
			Image.img_url==url)).order(-Image.date)
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
	def get_by_qid(cls, qid):
		question=Question.query(Question.q_id == qid)
		return question.fetch()

	@classmethod
	def get_by_user_all(cls, quser):
		question=Question.query(Question.q_user==quser).\
		order(-Question.edit_time).order(-Question.edit_time)
		return question.fetch()

	@classmethod
	def get_all(cls):
		question=Question.query().order(-Question.edit_time)
		return question.fetch()

	@classmethod
	def get_by_tag(cls, tag):
		question=Question.query(Question.q_tags.IN([tag])).order(-Question.edit_time)
		return question.fetch()

	@classmethod
	def get_by_tag_user(cls, tag, quser):
		question=Question.query(ndb.AND(Question.q_tags.IN([tag]), \
			Question.q_user==quser)).order(-Question.edit_time)
		return question.fetch()

class Answer(ndb.Model):
	a_user=ndb.StringProperty()
	a_id=ndb.StringProperty()
	q_id=ndb.StringProperty()
	a_content=ndb.TextProperty(indexed=False)
	create_time=ndb.DateTimeProperty(auto_now_add=True)
	edit_time=ndb.DateTimeProperty(auto_now_add=True)
	vp_num=ndb.IntegerProperty()
	vd_num=ndb.IntegerProperty()

	@classmethod
	def get_by_user_qid(cls, auser, qid):
		answer=Answer.query(ndb.AND(Answer.q_id==qid, Answer.a_user==auser) \
			).order(-Answer.edit_time)
		return answer.fetch()

	@classmethod
	def get_by_qid(cls, qid):
		answer=Answer.query(Answer.q_id==qid).order(-Answer.edit_time)
		return answer.fetch()
	
	@classmethod
	def get_by_aid(cls, aid):
		answer=Answer.query(Answer.a_id==aid)
		return answer.fetch()

	@classmethod
	def get_by_auser(cls, auser):
		answer=Answer.query(Answer.a_user==str(auser)).order(-Answer.edit_time)
		return answer.fetch()


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
			if str(v.vote).lower() == "up":
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
			if str(v.vote).lower() == "up":
				up_count+=1
			else:
				down_count+=1
		return (up_count, down_count)


