import multiprocessing
from nltk.tokenize import sent_tokenize
import re


class FindMatchesProcess(multiprocessing.Process):

	def __init__(self, query, formatted_emails_queue, matched_sentences_queue):
		multiprocessing.Process.__init__(self)
		self.word_deck = query.split(" OR ")
		self.formatted_emails_queue = formatted_emails_queue
		self.matched_sentences_queue = matched_sentences_queue

	def run(self):
		self.find_matches()

	def find_matches(self):
		index = 0
		(email, user) = self.formatted_emails_queue.get()

		for word in self.word_deck:
			if word.lower() in email.lower():
				self.find_sentences(index, email, user)
				break
			index += 1

	def find_sentences(self, word_index, email, user):
		"""This method returns a generator of sentences that contain the
		word passed in as a parameter"""
		words_to_search = self.word_deck[word_index:]
		sentence_list = sent_tokenize(email)

		for sentence in sentence_list:
			for word_to_search in words_to_search:
				if word_to_search.lower() in sentence.lower():
					FindMatchesProcess.clean_sentence(sentence)
					# add to pipe
					self.matched_sentences_queue.put([sentence, word_to_search, user])
					break

	@staticmethod
	def clean_sentence(sentence):
		space_pattern = re.compile('\s{2,}')
		sentence = sentence.replace('\n', ' ')
		sentence = sentence.replace('=20', ' ')
		sentence = re.sub(space_pattern, ' ', sentence)
		return sentence

	def raise_exc(self, type):
		raise type

