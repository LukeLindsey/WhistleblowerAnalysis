from SearchInterface import SearchInterface
# from EnronThread import EnronThread
# from dbFacade import dbFacade
# from Scorer import Scorer
# import EnronSearch
import time
import multiprocessing
from FindEmailProcess import FindEmailProcess
from FindMatchesProcess import FindMatchesProcess
from ScoreSentencesProcess import ScoreSentencesProcess
from SendSentencesThread import SendSentencesThread
from SendUsersThread import SendUsersThread


class EnronInterface(SearchInterface):

	"""
	Starts search crawling threads with inputed query string.
	"""
	def search(self, query=None, args=None):
		# type checking
		if not isinstance(query, str):
			raise TypeError('Query must be a string')
		elif not isinstance(args, dict):
			raise TypeError('Args must be a dictionary')

		formatted_emails_put, formatted_emails_get = multiprocessing.Pipe()
		matched_sentences_put, matched_sentences_get = multiprocessing.Pipe()
		scored_sentences_put, scored_sentences_get = multiprocessing.Pipe()
		usernames_put, usernames_get = multiprocessing.Pipe()


		self.find_email_process = FindEmailProcess(args['folder_location'], formatted_emails_put, self.db, usernames_put)

		self.find_matches_process = FindMatchesProcess(query, formatted_emails_get, matched_sentences_put)

		self.score_sentences_process = ScoreSentencesProcess(self.scorer, matched_sentences_get, scored_sentences_put)

		# change this to thread and add a name pipe
		self.send_database_thread = SendSentencesThread(self.db, scored_sentences_get)

		self.send_users_thread = SendUsersThread(self.db, usernames_get)

		self.find_email_process.start()
		self.find_matches_process.start()
		self.score_sentences_process.start()
		self.send_database_thread.start()
		self.send_users_thread.start()

		self.find_email_process.join()
		self.find_matches_process.join()
		self.score_sentences_process.join()
		self.send_database_thread.join()
		self.send_users_thread.join()

		time.sleep(5)

	'''
	Ends search crawling threads; 
	waits for them to terminate before continuing.
	'''
	def stop_search(self):
		print "Closing threads.."
		try:		
			self.find_email_process.raise_exc(KeyboardInterrupt)
			self.find_matches_process.raise_exc(KeyboardInterrupt)
			self.score_sentences_process.raise_exc(KeyboardInterrupt)
			self.send_database_process.raise_exc(KeyboardInterrupt)
		except: #add a more specific one
			pass # add a fail here

		while self.find_email_process.is_alive() or self.find_matches_process.is_alive() or \
				self.score_sentences_process.is_alive() or self.send_database_process.is_alive():
			time.sleep(1)
		self.find_email_process.join()
		self.find_matches_process.join()
		self.score_sentences_process.join()
		self.send_database_process.join()

