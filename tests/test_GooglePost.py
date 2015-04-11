import unittest
from SocialNetworkSearch.GooglePlus.GooglePost import GooglePost

"""__author__ = 'LukeLindsey' """


class test_GooglePost(unittest.TestCase):

	def test_create_instance_with_result_argument_missing(self):
		try:
			post = GooglePost()
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_invalid_result_argument(self):
		try:
			post = GooglePost(result="Invalid")
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_missing_actor_from_result(self):
		try:
			post = GooglePost(result={'object': {'content': ''}, 'updated': ''})
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_missing_object_from_result(self):
		try:
			post = GooglePost(result={'actor': {'displayName': ''}, 'updated': ''})
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_missing_date_from_result(self):
		try:
			post = GooglePost(result={'actor': {'displayName': ''}, 'object': {'content': ''}})
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_valid_args(self):
		post = GooglePost(result={'actor': {'displayName': ''}, 'object': {'content': ''}, 'updated': ''})