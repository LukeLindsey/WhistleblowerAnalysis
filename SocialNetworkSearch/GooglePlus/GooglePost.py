"""
This class handles all operations involving
the Twitter API.

@author: Luke Lindsey
@date: 10 Mar 2015
"""


class GooglePost(object):

	def __init__(self, result):
		actor = result["actor"]
		self.author = actor["displayName"]
		my_object = result["object"]
		self.post = my_object["content"]
		self.post = self.post.replace('\\ufeff', '')  # remove endian order code
		self.date = result["updated"]

# might add location and/or url
