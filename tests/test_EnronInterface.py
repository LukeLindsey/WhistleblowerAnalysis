import unittest
from EnronSearch.EnronInterface import EnronInterface
from dbFacade import dbFacade
from Scorer import Scorer
from Attribute import Attribute
from SearchPacket import SearchPacket

"""__author__ = 'LukeLindsey' """


class test_GooglePlusThread(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.args = {'folder_location': '/users/lukelindsey/Downloads/enron_mail_20110402/maildir'}
		self.query = "pizza OR tacos OR burgers OR fries"
		self.e = EnronInterface()

	def test_search_with_missing_params(self):
		try:
			self.e.search()
			self.fail()
		except TypeError:
			pass

	def test_search_with_missing_query(self):
		try:
			self.e.search(None, self.args)
			self.fail()
		except TypeError:
			pass

	def test_search_with_missing_args(self):
		try:
			self.e.search(self.query, None)
			self.fail()
		except TypeError:
			pass

	def test_search_with_invalid_query(self):
		try:
			self.e.search(['invalid'], self.args)
			self.fail()
		except TypeError:
			pass

	def test_search_with_invalid_args(self):
		try:
			self.e.search(self.query, "Invalid")
			self.fail()
		except TypeError:
			pass
