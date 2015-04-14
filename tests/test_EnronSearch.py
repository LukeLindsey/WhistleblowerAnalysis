import unittest
from EnronSearch.EnronSearch import EnronSearch
from dbFacade import dbFacade
from Scorer import Scorer
from Attribute import Attribute
from SearchPacket import SearchPacket

"""__author__ = 'LukeLindsey' """


class test_EnronSearch(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.words = ['pizza', 'tacos', 'burgers', 'fries']
		weights = [1, 3, 2, 2]
		sentiments = [1, 1, 1, 1]
		self.query = "pizza OR tacos OR burgers OR fries"
		attribute = Attribute("Attribute1", 1, self.words, weights, sentiments)
		attributes = [attribute]
		search_packet = SearchPacket(attributes)
		self.scorer = Scorer(search_packet)
		self.directory = '/users/lukelindsey/Downloads/enron_mail_20110402/maildir'

		self.db = dbFacade()
		self.e = EnronSearch(self.words, self.db, self.scorer, self.directory)
		# self.db.connect()
		# self.db.create_keyspace_and_schema()

	def test_create_instance_with_valid_args(self):
		EnronSearch(self.words, self.db, self.scorer, self.directory)

	def test_create_instance_missing_params(self):
		try:
			EnronSearch()
			self.fail()
		except TypeError:
			pass

	def test_create_instance_missing_db(self):
		try:
			EnronSearch(self.words, None, self.scorer, self.directory)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_missing_scorer(self):
		try:
			EnronSearch(self.words, self.db, None, self.directory)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_missing_directory(self):
		try:
			EnronSearch(self.words, self.db, self.scorer, None)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_missing_words(self):
		try:
			EnronSearch(None, self.db, self.scorer, self.directory)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_invalid_db(self):
		try:
			EnronSearch(self.words, "Invalid", self.scorer, self.directory)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_invalid_scorer(self):
		try:
			EnronSearch(self.words, self.db, "Invalid", self.directory)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_invalid_directory(self):
		try:
			EnronSearch(self.words, self.db, self.scorer, 4)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_invalid_words_non_list(self):
		try:
			EnronSearch("Invalid", self.db, self.scorer, self.directory)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_invalid_words_numbers(self):
		try:
			EnronSearch([1, 2, 3], self.db, self.scorer, self.directory)
			self.fail()
		except TypeError:
			pass

	# extract sentences
	def test_extract_sentences_entire_words_list(self):
		expected = "I love pizza."
		total = "I love pizza. This is the second sentence."
		actuals = self.e.extract_sentences(0, total)
		for actual in actuals:
			self.assertEqual(expected, actual)

	def test_extract_sentences_partial_words_list(self):
		expected = "We are having tacos!"
		total = "I love pizza. This is the second sentence. We are having tacos!"
		actuals = self.e.extract_sentences(1, total)
		for actual in actuals:
			self.assertEqual(expected, actual)

	def test_should_not_return_repeat(self):
		expected = "Pizza and fries are pretty good."
		total = "Pizza and fries are pretty good. This is the second sentence."
		actuals = self.e.extract_sentences(0, total)
		for actual in actuals:
			self.assertEqual(expected, actual)

	# clean sentences
	def test_clean_sentences_lots_of_spaces(self):
		expected = "Trying to remove the spaces."
		input_string = "Trying     to       remove the spaces."
		actual = EnronSearch.clean_sentence(input_string)
		self.assertEqual(expected, actual)

	def test_clean_sentences_lots_of_newlines(self):
		expected = "Trying to remove the spaces."
		input_string = "Trying \n\n\n\n\n\nto remove the\n spaces."
		actual = EnronSearch.clean_sentence(input_string)
		self.assertEqual(expected, actual)

	def test_clean_sentences_lots_of_spaces_and_newlines(self):
		expected = "Trying to remove the spaces."
		input_string = "Trying\n     to      \n\n\n remove the\n\n\n spaces."
		actual = EnronSearch.clean_sentence(input_string)
		self.assertEqual(expected, actual)