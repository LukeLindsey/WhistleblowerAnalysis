from SearchInterface import SearchInterface
from EnronThread import EnronThread
from dbFacade import dbFacade
from Scorer import Scorer
import EnronSearch
import time
import threading
import multiprocessing


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

		formattedEmails = multiprocessing.Pipe()
		matchedSentences = multiprocessing.Pipe()
		scoredSentences = multiprocessing.Pipe()


		self.findEmailProcess = FindEmailProcess(args['folder_location'], formattedEmails, self.db)

		self.findMatchesProcess = FindMatchesProcess(query, formattedEmails, matchedSentences)

		self.scoreSentencesProcess = ScoreSentencesProcess(self.scorer, matchedSentences, scoredSentences)

		self.sendDatabaseProcess = SendDatabaseProcess(self.db, scoredSentences)

		self.findEmailProcess.start()
		self.findMatchesProcess.start()
		self.scoreSentencesProcess.start()
		self.sendDatabaseProcess.start()

		self.findEmailProcess.join()
		self.findMatchesProcess.join()
		self.scoreSentencesProcess.join()
		self.sendDatabaseProcess.join()

		time.sleep(5)

	'''
	Ends search crawling threads; 
	waits for them to terminate before continuing.
	'''
	def stop_search(self):
		print "Closing threads.."
		try:		
			self.findEmailProcess.raiseExc(KeyboardInterrupt)
			self.findMatchesProcess.raiseExc(KeyboardInterrupt)
			self.scoreSentencesProcess.raiseExc(KeyboardInterrupt)
			self.sendDatabaseProcess.raiseExc(KeyboardInterrupt)
		except: #add a more specific one
			pass

		while self.findEmailProcess.isAlive() || self.findMatchesProcess.isAlive() || self.scoreSentencesProcess.isAlive() || self.sendDatabaseProcess.isAlive():
			time.sleep(1)
		self.findEmailProcess.join()
		self.findMatchesProcess.join()
		self.scoreSentencesProcess.join()
		self.sendDatabaseProcess.join()

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
