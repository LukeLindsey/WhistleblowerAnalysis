from GooglePlusSearch import GooglePlusSearch
import sys
import traceback


"""
This class defines a basic Google+ api search.
No special search parameters are used (i.e. date range).

@author: Luke Lindsey
@date: 14 March 2015
"""


class BasicSearch(GooglePlusSearch):

	def search(self):
		next_page_token = self.get_first_20_results()

		if self.postCount < 20:
			return self.postCount

		try:
			self.get_next_20_results(next_page_token)
		except KeyboardInterrupt:
			print('\n Google+: Terminated by user (search)\n')
		except Exception as e:
			print('\n Google+: Terminated due to error\n')
			print(e)

		return self.postCount

	def get_first_20_results(self):
		next_page_token = ''
		try:
			results_total = super(BasicSearch, self).get_20_search_results()
			results = results_total["items"]

			if self.location_search:
				results = super(BasicSearch, self).filter_by_location(results, self.location_center, self.location_radius)

			if self.date_search:
				results = super(BasicSearch, self).filter_by_date(results, self.from_date)

			posts = super(BasicSearch, self).create_google_objects(results)
			super(BasicSearch, self).store_posts_in_database(posts)
			next_page_token = results_total["nextPageToken"]
		except KeyboardInterrupt:
			print ('\n Terminated by user (search)\n')
		except KeyError:
			next_page_token = ''

		return next_page_token

	def get_next_20_results(self, page_token):
		while page_token != '':

			try:
				results_total = super(BasicSearch, self).get_20_search_results(page_token)
				results = results_total["items"]

				'''if self.location_search:
					results = super(BasicSearch, self).filter_by_location(results, self.location_center, self.location_radius)

				if self.date_search:
					results = super(BasicSearch, self).filter_by_date(results, self.from_date)'''

				posts = super(BasicSearch, self).create_google_objects(results)
				super(BasicSearch, self).store_posts_in_database(posts)
			except Exception as e:
				#print "failing at line 73 in BasicGooglePlusSearch"
				#exc_type, exc_obj, exc_tb = sys.exc_info()
				#print 'type: ' + str(exc_type)
				#print(e)
				traceback.print_exception(*exc_info)
				#sys.exit(0)
			try:
				page_token = results_total["nextPageToken"]
			except KeyError:
				page_token = ''
