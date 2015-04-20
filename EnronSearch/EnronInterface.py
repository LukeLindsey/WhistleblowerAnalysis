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
from SendDatabaseProcess import SendDatabaseProcess


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

		formatted_emails = multiprocessing.Pipe()
		matched_sentences = multiprocessing.Pipe()
		scored_sentences = multiprocessing.Pipe()


		self.find_email_process = FindEmailProcess(args['folder_location'], formatted_emails, self.db)

		self.find_matches_process = FindMatchesProcess(query, formatted_emails, matched_sentences)

		self.score_sentences_process = ScoreSentencesProcess(self.scorer, matched_sentences, scored_sentences)

		self.send_database_process = SendDatabaseProcess(self.db, scored_sentences)

		self.find_email_process.start()
		self.find_matches_process.start()
		self.score_sentences_process.start()
		self.send_database_process.start()

		self.find_email_process.join()
		self.find_matches_process.join()
		self.score_sentences_process.join()
		self.send_database_process.join()

		time.sleep(5)

	'''
	Ends search crawling threads; 
	waits for them to terminate before continuing.
	'''
	def stop_search(self):
		print "Closing threads.."
		try:		
			self.find_email_process.raiseExc(KeyboardInterrupt)
			self.find_matches_process.raiseExc(KeyboardInterrupt)
			self.score_sentences_process.raiseExc(KeyboardInterrupt)
			self.send_database_process.raiseExc(KeyboardInterrupt)
		except: #add a more specific one
			pass

		while self.find_email_process.is_alive() or self.find_matches_process.is_alive() or self.score_sentences_process.is_alive() or self.send_database_process.is_alive():
			time.sleep(1)
		self.find_email_process.join()
		self.find_matches_process.join()
		self.score_sentences_process.join()
		self.send_database_process.join()

