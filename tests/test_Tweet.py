import unittest
import twitter
from SocialNetworkSearch.Tweet import Tweet
from Scorer import Scorer
from Attribute import Attribute
from SearchPacket import SearchPacket

class test_Tweet(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		words = ['pizza', 'tacos', 'burgers', 'fries']
		weights = [1,3,2,2]
		sentiments = [1,1,1,1]    
		self.args = { 'location' : None, 'since' : None, 'until' : None }
		attribute = Attribute("Attribute1", 1, words, weights, sentiments)
		attributes = [attribute]
		search_packet = SearchPacket(attributes)
		self.scorer = Scorer(search_packet)

	def test_create_instance_with_scorer_argument_missing(self):	
		try:
			tweet = Tweet(api_data=None)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_api_data_argument_missing(self):
		try:
			tweet = Tweet(scorer=None)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_invalid_scorer_argument(self):
		try:
			tweet = Tweet(scorer="Invalid", api_data={})
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_invalid_api_data_argument(self):		
		try:
			tweet = Tweet(scorer = self.scorer, api_data="Invalid")
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_invalid_api_data_with_missing_user_key(self):		
		try:
			tweet = Tweet(scorer = self.scorer, api_data={'text' : 'post content'})
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_invalid_api_data_with_missing_text_key(self):		
		try:
			tweet = Tweet(scorer = self.scorer, api_data={'user' : {}})
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_invalid_api_data_with_missing_screen_name_key(self):		
		try:
			tweet = Tweet(scorer = self.scorer, api_data={'user' : {}, 'text' : 'post content'})
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_valid_arguments(self):
		api_data={'user' : {'screen_name' : 'bob'}, 'text' : 'post content'}
		tweet = Tweet(scorer = self.scorer, api_data = api_data)

if __name__ == '__main__':
    unittest.main()

