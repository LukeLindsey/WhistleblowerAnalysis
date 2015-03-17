from dbFacade import dbFacade
from Scorer import Scorer

class SearchInterface:

	def __init__(self):
		self.db = dbFacade()
		self.db.connect()
		self.db.create_keyspace_and_schema()

	def initialize_scorer(self, search_packet):
		self.scorer = Scorer(search_packet)

	'''
	Retrieves users, calculates user scores, 
	updates score in database, and prints top 10 results.
	'''	
	def score(self):
		print "Scoring..\n"
		users = self.db.get_users_dict()
		scores = self.db.calculate_user_scores(users)
		self.db.populate_user_scores(users, scores)
