"""
This class handles all operations involving
the Twitter API.

@author: Luke Lindsey
@date: 10 Mar 2015
"""


class GooglePost(object):

	def __init__(self, result=None):
		if result is None:
			raise TypeError('\'result\' is required for GooglePost.')
		elif not isinstance(result, dict):
			raise TypeError('\'result\' passed in must be a dict.')
		try:
			actor = result["actor"]
			self.author = actor["displayName"]
			my_object = result["object"]
			self.post = my_object["content"]
			self.post = self.post.replace('\\ufeff', '')  # remove endian order code
			self.date = result["updated"]
		except KeyError:
			raise TypeError('\'result\' is not a valid result from G+. Causes KeyError.')

# might add location and/or url
