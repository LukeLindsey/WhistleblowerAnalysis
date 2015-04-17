from dbFacade import dbFacade
from Scorer import Scorer
from SocialNetworkSearch.GooglePlus.GooglePlusThread import GooglePlusThread
from SocialNetworkSearch.TwitterThread import TwitterThread
import threading
import time

class SearchInterface:

	threads = []

	def __init__(self):
		self.db = dbFacade()
		self.db.connect()
		self.db.create_keyspace_and_schema()

	def initialize_scorer(self, search_packet):
		self.scorer = Scorer(search_packet)

	'''
	Starts search crawling threads with inputed query string.
	'''
	def search(self, query, args):
		self.threads = []
		if args['GooglePlus']:
			self.threads.append(GooglePlusThread(self.db, self.scorer, query, args))
		if args['Twitter']:
			self.threads.append(TwitterThread(self.db, self.scorer, query, args))

		for thread in self.threads:
			thread.start()
		for thread in self.threads:
			thread.join()

	'''
	Ends search crawling threads; 
	waits for them to terminate before continuing.
	'''
	def stop_search(self):
		print "Closing threads.."
		for thread in self.threads:
			try:		
				thread.raiseExc(KeyboardInterrupt)
			except threading.ThreadError:
				pass

		for thread in self.threads:
			while thread.isAlive():
				time.sleep(1)
			thread.join()

	'''
	Retrieves users, calculates user scores, and
	updates score in database
	'''	
	def score(self, progress_que):
		print "Scoring..\n"
		users = self.db.get_users_dict()
		progress_que.put(33)
		self.populate_user_scores(users, progress_que)

	def populate_user_scores(self, users, progress_que):
		completion = 0.0
		step_progress = ((1.0/len(users))*0.67)*100

		for user in users:
			self.update_user_score(user)
			
			completion = completion + step_progress
			if completion >= 1:
				progress_que.put(1)
				completion = completion - 1
				if completion < 0:
					completion = 0.0

	def update_user_score(self, user):
		posts = self.db.get_posts(user['username'])
		total = 0
		for post in posts:
			total += post['score']
		user['score'] = total
		
		self.db.insert_user_score(
			user['username'], 
			user['score'], 
			user['website'])


