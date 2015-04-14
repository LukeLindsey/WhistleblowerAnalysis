from SearchInterface import SearchInterface
from EnronThread import EnronThread
from dbFacade import dbFacade
from Scorer import Scorer
import EnronSearch
import time
import threading


class EnronInterface(SearchInterface):

	'''
	Starts search crawling threads with inputed query string.
	'''
	def search(self, query=None, args=None):
		# type checking
		if not isinstance(query, str):
			raise TypeError('Query must be a string')
		elif not isinstance(args, dict):
			raise TypeError('Args must be a dictionary')

		self.thread = EnronThread(self.db, self.scorer, query, args)
		self.thread.start()
		self.thread.join()
		time.sleep(5)

	'''
	Ends search crawling threads; 
	waits for them to terminate before continuing.
	'''
	def stop_search(self):
		print "Closing threads.."
		try:		
			self.thread.raiseExc(KeyboardInterrupt)
		except threading.ThreadError:
			pass

		while self.thread.isAlive():
			time.sleep(1)
		self.thread.join()

	@staticmethod
	def print_statistics(enron_search):
		total_time = enron_search.end_time - enron_search.start_time
		total_seconds = total_time.seconds
		hours = total_seconds // 3600
		total_seconds = total_seconds % 3600
		minutes = total_seconds // 60
		seconds = total_seconds % 60

		print "Searching Enron took: " + str(hours) + " hours, " + str(minutes) + \
		      " minutes, and " + str(seconds) + " seconds."

		print "Searched " + str(enron_search.total_users) + " users."
		print "Searched " + str(enron_search.total_emails) + " emails."
		print str(enron_search.total_sentences_matched) + " sentences were matches."
