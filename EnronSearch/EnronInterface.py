from SearchInterface import SearchInterface
# from EnronThread import EnronThread
# from dbFacade import dbFacade
# from Scorer import Scorer
# import EnronSearch
import time
import multiprocessing
import threading
from FindEmailProcess import FindEmailProcess
from FindMatchesProcess import FindMatchesProcess
from ScoreSentencesProcess import ScoreSentencesProcess
from SendSentencesThread import SendSentencesThread
from SendUsersThread import SendUsersThread
from datetime import datetime


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

		formatted_emails = multiprocessing.Queue()
		matched_sentences = multiprocessing.Queue()
		scored_sentences = multiprocessing.Queue()
		usernames = multiprocessing.Queue()

		start_time = datetime.now()


		self.find_email_process = FindEmailProcess(args['folder_location'], formatted_emails, usernames, self.db)

		self.find_matches_process = FindMatchesProcess(query, formatted_emails, matched_sentences)

		self.score_sentences_process = ScoreSentencesProcess(self.scorer, matched_sentences, scored_sentences)

		self.send_database_thread = SendSentencesThread(self.db, scored_sentences)

		self.send_users_thread = SendUsersThread(self.db, usernames)

		self.start()

		self.join()

		print "DONE WITH ALL"

		end_time = datetime.now()

		total = end_time - start_time
		print total

		time.sleep(5)

	'''Starts all the threads and processes'''
	def start(self):
		self.find_email_process.start()
		self.find_matches_process.start()
		self.score_sentences_process.start()
		self.send_database_thread.start()
		self.send_users_thread.start()

	'''Joins all the threads and processes'''
	def join(self):
		self.find_email_process.join()
		self.find_matches_process.join()
		self.score_sentences_process.join()
		self.send_database_thread.join()
		self.send_users_thread.join()

	'''
	Ends search crawling threads; 
	waits for them to terminate before continuing.
	'''
	def stop_search(self):
		print "Closing threads.."
		try:		
			self.find_email_process.terminate()
			self.find_matches_process.terminate()
			self.score_sentences_process.terminate()
			self.send_database_thread.raiseExc(KeyboardInterrupt)
			self.send_users_thread.raiseExc(KeyboardInterrupt)
		except threading.ThreadError:
			pass

		while self.find_email_process.is_alive() or self.find_matches_process.is_alive() or \
				self.score_sentences_process.is_alive() or self.send_database_thread.is_alive()\
				or self.send_users_thread.is_alive():
			time.sleep(1)
		self.find_email_process.join()
		self.find_matches_process.join()
		self.score_sentences_process.join()
		self.send_database_thread.join()
		self.send_users_thread.join()

