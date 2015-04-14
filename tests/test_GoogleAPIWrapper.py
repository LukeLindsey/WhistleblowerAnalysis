import unittest
from SocialNetworkSearch.GooglePlus.GoogleAPIWrapper import GoogleAPIWrapper

"""__author__ = 'LukeLindsey' """


class test_GoogleAPIWrapper(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		# dictionary for containing the GET query parameters.
		self.payload = {}
		# setting the query parameter
		self.payload["query"] = "hello"
		# setting the google plus api key
		self.payload["key"] = "AIzaSyDAzvL9nU0nv7j84UfvWXygwXO9hDbKYDk"
		# setting the parameter for the number of returned results to 20
		self.payload["maxResults"] = 20
		# setting the order of the returned results to recent.
		self.payload["orderBy"] = "recent"
		# setting the language parameter to English, so that the returned activity feeds are only in english
		self.payload["language"] = "en"

	def test_default_search_valid_params(self):
		GoogleAPIWrapper.default_search(self.payload)
		pass

	def test_default_search_missing_parameters(self):
		try:
			GoogleAPIWrapper.default_search(None)
			self.fail()
		except AssertionError:
			pass

	def test_default_search_missing_query(self):
		try:
			GoogleAPIWrapper.default_search({})
			self.fail()
		except AssertionError:
			pass





