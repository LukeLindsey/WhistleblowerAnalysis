from SearchInterface import SearchInterface
from TwitterThread import TwitterThread
from TwitterGeoPics.Geocoder import Geocoder
import time
import thread
import threading

'''
This class serves as an interface for controlling
social media crawling and analysis

@author: Brenden Romanowski
@date: 24 Feb 2015
'''

class Interface(SearchInterface):
	
	'''
	Starts search crawling threads with inputed query string.
	'''
	def search(self, query, args):
		self.twitterThread = TwitterThread(self.db, self.scorer, query, args)
		self.twitterThread.start()
		self.twitterThread.join()

	'''
	Ends search crawling threads; 
	waits for them to terminate before continuing.
	'''
	def stop_search(self):
		print "Closing threads.."
		try:		
			self.twitterThread.raiseExc(KeyboardInterrupt)
		except threading.ThreadError:
			pass

		while self.twitterThread.isAlive():
			time.sleep(1)
		self.twitterThread.join()
