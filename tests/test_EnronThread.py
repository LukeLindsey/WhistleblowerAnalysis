import unittest
from EnronSearch.EnronThread import EnronThread
from dbFacade import dbFacade
from Scorer import Scorer
from Attribute import Attribute
from SearchPacket import SearchPacket

"""__author__ = 'LukeLindsey' """


class test_EnronThread(unittest.TestCase):

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
		self.args = {'folder_location': '/users/lukelindsey/Downloads/enron_mail_20110402/maildir'}

		self.db = dbFacade()
		# self.db.connect()
		# self.db.create_keyspace_and_schema()

	def test_create_instance_with_valid_args(self):
		EnronThread(db=self.db, scorer=self.scorer, query=self.query, args=self.args)

	def test_create_instance_missing_params(self):
		try:
			EnronThread()
			self.fail()
		except TypeError:
			pass

	def test_create_instance_missing_db(self):
		try:
			EnronThread(None, self.scorer, self.query, self.args)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_missing_scorer(self):
		try:
			EnronThread(self.db, None, self.query, self.args)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_missing_query(self):
		try:
			EnronThread(self.db, self.scorer, None, self.args)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_missing_args(self):
		try:
			EnronThread(self.db, self.scorer, self.query, None)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_invalid_db(self):
		try:
			EnronThread("Invalid", self.scorer, self.query, self.args)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_invalid_scorer(self):
		try:
			EnronThread(self.db, "Invalid", self.query, self.args)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_invalid_query(self):
		try:
			EnronThread(self.db, self.scorer, 4, self.args)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_invalid_args(self):
		try:
			EnronThread(self.db, self.scorer, self.query, {})
			self.fail()
		except KeyError:
			pass