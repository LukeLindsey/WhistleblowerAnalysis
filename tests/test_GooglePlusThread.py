import unittest
from SocialNetworkSearch.GooglePlus.GooglePlusThread import GooglePlusThread
#from SocialNetworkSearch.GooglePlus.GoogleAPIWrapper import GoogleAPIWrapper
from dbFacade import dbFacade
from Scorer import Scorer
from Attribute import Attribute
from SearchPacket import SearchPacket

"""__author__ = 'LukeLindsey' """


class test_GooglePlusThread(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		words = ['pizza', 'tacos', 'burgers', 'fries']
		weights = [1, 3, 2, 2]
		sentiments = [1, 1, 1, 1]
		self.query = "pizza OR tacos OR burgers OR fries"
		attribute = Attribute("Attribute1", 1, words, weights, sentiments)
		attributes = [attribute]
		search_packet = SearchPacket(attributes)
		self.scorer = Scorer(search_packet)

		self.db = dbFacade()
		# self.db.connect()
		# self.db.create_keyspace_and_schema()
		#self.api_key = GoogleAPIWrapper.get_api_key()

	def test_create_instance_with_valid_args(self):
		GooglePlusThread(db=self.db, scorer=self.scorer, query=self.query)

	def test_create_instance_missing_args(self):
		try:
			GooglePlusThread()
			self.fail()
		except TypeError:
			pass

	def test_create_instance_missing_db(self):
		try:
			GooglePlusThread(None, self.scorer, self.query)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_missing_scorer(self):
		try:
			GooglePlusThread(self.db, None, self.query)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_missing_query(self):
		try:
			GooglePlusThread(self.db, self.scorer, None)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_invalid_db(self):
		try:
			GooglePlusThread("Invalid", self.scorer, self.query)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_invalid_scorer(self):
		try:
			GooglePlusThread(self.db, "Invalid", self.query)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_invalid_query(self):
		try:
			GooglePlusThread(self.db, self.scorer, 4)
			self.fail()
		except TypeError:
			pass