import os
import emailformat
from datetime import datetime
from nltk.tokenize import sent_tokenize


class EnronSearch:

	def __init__(self, word_deck, db, scorer, email_main_directory):
		self.word_deck = word_deck
		print self.word_deck
		self.email_main_directory = email_main_directory + '/'
		self.db = db
		self.scorer = scorer
		self.total_users = 0
		self.total_emails = 0
		self.total_sentences_matched = 0
		self.start_time = datetime.now()
		self.end_time = datetime.now()

	def search_enron(self):

		my_sent_folder = r'/sent/'#, r'/sent_items/']  # there are more sent folders than this, let's start small though

		user_directory_list = os.listdir(self.email_main_directory)

		for user_dir in user_directory_list:
			#for my_sent_folder in my_sent_folders:
			for sent_folder, no_directories, email_files in os.walk(self.email_main_directory + user_dir + my_sent_folder):
				for email_file_name in email_files:
					email_file = open((sent_folder + email_file_name), 'r')
					email = email_file.read()
					email_file.close()
					self.process_email(email, user_dir)
					self.total_emails += 1
			print user_dir

			self.db.add_user(user_dir, 0, 'Enron')
			self.total_users += 1

		self.end_time = datetime.now()

	def process_email(self, email, user):

		email = emailformat.format_email(email)  # remove the junk

		index = 0

		for word in self.word_deck:
			if word.lower() in email.lower():
				sentences = EnronSearch.extract_sentences(self.word_deck[index:], email)

				for sentence in sentences:
					score = float(self.scorer.score(sentence))
					self.db.add_post(user, 'Enron', sentence.replace("'", "''"), word, score)
					self.total_sentences_matched += 1
			index += 1

	@staticmethod
	def extract_sentences(words_to_search, email):
		"""This method returns a generator of sentences that contain the
		word passed in as a parameter"""

		sentence_list = sent_tokenize(email)
		for sentence in sentence_list:
			for word_to_search in words_to_search:
				if word_to_search.lower() in sentence.lower():
					yield sentence
					break
