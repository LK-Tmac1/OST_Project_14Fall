from google.appengine.ext import ndb


####Image
class Image(ndb.Model):
	image_url=ndb.StringProperty()
	image_user=ndb.StringProperty()
	image_file = ndb.BlobProperty()
	filename=ndb.StringProperty()
	upload_time=ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_img_by_user(cls, user):
		target_img=Image.query(Image.image_user == user).order(-Image.upload_time)
		return target_img.fetch()

	@classmethod
	def get_img_by_url(cls, url):
		target_img=Image.query(Image.image_url==url).order(-Image.upload_time)
		return target_img.fetch()

	@classmethod
	def get_img_all(cls):
		imagelist= Image.query().order(-Image.upload_time)
		return imagelist.fetch()

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
	v_diff = ndb.ComputedProperty(lambda self: self.vp_num - self.vd_num)

	@classmethod
	def get_by_qid(cls, qid):
		question=Question.query(Question.q_id == qid)
		return question.fetch()

	@classmethod
	def get_by_user(cls, quser):
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
	def get_by_tag_user(cls, tag, user):
		question=Question.query(ndb.AND(Question.q_tags.IN[tag], Question.q_user==user)).order(-Question.edit_time)
		return question.fetch()

	@classmethod
	def get_by_tag_user(cls, tag, user):
		question=Question.query(ndb.AND(Question.q_tags.IN([tag]), Question.q_user==user)).order(-Question.edit_time)
		return question.fetch()

####Answer
class Answer(ndb.Model):
	a_user=ndb.StringProperty()
	a_id=ndb.StringProperty()
	q_id=ndb.StringProperty()
	a_content=ndb.TextProperty(indexed=False)
	create_time=ndb.DateTimeProperty(auto_now_add=True)
	edit_time=ndb.DateTimeProperty(auto_now_add=True)
	vp_num=ndb.IntegerProperty()
	vd_num=ndb.IntegerProperty()
	v_diff = ndb.ComputedProperty(lambda self: self.vp_num - self.vd_num)

	@classmethod
	def get_by_user_qid(cls, auser, qid):
		answer=Answer.query(ndb.AND(Answer.q_id==qid, Answer.a_user==auser) \
			).order(-Answer.v_diff).order(-Answer.edit_time)
		return answer.fetch()

	@classmethod
	def get_by_qid(cls, qid):
		answer=Answer.query(Answer.q_id==qid).order(-Answer.v_diff).order(-Answer.edit_time)
		return answer.fetch()
	
	@classmethod
	def get_by_aid(cls, aid):
		answer=Answer.query(Answer.a_id==aid)
		return answer.fetch()

	@classmethod
	def get_by_auser(cls, auser):
		answer=Answer.query(Answer.a_user==str(auser)).order(-Answer.v_diff).order(-Answer.edit_time)
		return answer.fetch()

####Vote
class Vote(ndb.Model):
	up_down=ndb.StringProperty()
	q_id=ndb.StringProperty()
	a_id=ndb.StringProperty()
	v_user=ndb.StringProperty()
	v_time=ndb.DateTimeProperty()	

	@classmethod
	def get_all_vote(cls):
		vote=Vote.query().order(-Vote.v_time)
		return vote.fetch()

	@classmethod
	def get_user_all_vote(cls, user):
		vote=Vote.query(Vote.v_user==user).order(-Vote.v_time)
		return vote.fetch()
	
	@classmethod
	def get_q_all_vote(cls):
		vote=Vote.query(Vote.aid==None).order(-Vote.v_time)
		return vote.fetch()

	@classmethod
	def get_a_all_vote(cls):
		vote=Vote.query(Vote.qid==None).order(-Vote.v_time)
		return vote.fetch()

	@classmethod
	def get_user_vote_q(cls, user, qid):
		vote=Vote.query(ndb.AND(Vote.v_user==user, Vote.q_id==qid)).order(-Vote.v_time)
		return vote.fetch()

	@classmethod
	def get_user_vote_a(cls, user, aid):
		vote=Vote.query(ndb.AND(Vote.v_user==user, Vote.a_id==aid)).order(-Vote.v_time)
		return vote.fetch()

	@classmethod
	def get_user_vote_all_q(cls, user):
		vote=Vote.query(ndb.AND(Vote.v_user==user, Vote.a_id==None)).order(-Vote.v_time)
		return vote.fetch()

	@classmethod
	def get_user_vote_all_a(cls, user):
		vote=Vote.query(ndb.AND(Vote.v_user==user, Vote.q_id==None)).order(-Vote.v_time)
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
	def get_a_vote(cls, aid):
		up_count=0
		down_count=0
		vote=Vote.query(ndb.AND(Vote.q_id==qid, Vote.a_id==aid))
		for v in vote.fetch():
			if str(v.vote).lower() == "up":
				up_count+=1
			else:
				down_count+=1
		return (up_count, down_count)


