#from nltk.corpus import movie_reviews
from textblob import TextBlob, Word
from SearchPacket import SearchPacket
from TextPreprocessor import TextPreprocessor

'''
This class will be fed words and their significance.
It will score a sentence based on whether those words appear,
and if they do, how significant they are to our attribute.

@author:  Justin A. Middleton
@date:    24 Feb 2015
'''
class Scorer():
	'''
	What I expect: a list of tuples
		A SearchPacket with attributes.
	'''
	def __init__(self, searchPacket):      
		self.packet = searchPacket
					
	'''
	Scores an input sentence, currently using the pattern analyzer
	as part of text blob. 
	Ignore subjectivity. Use absolute value of polarity.
	'''
	def score(self, text):
		processed = TextPreprocessor(text)
		bagOfWords = processed.get_words() #LINE WILL CHANGE
		polarity = TextBlob(processed.get_raw()).sentiment.polarity
		score = 0
		
		for attr in self.packet.getAttributes():
			attrScore = 0
			for i in range(0, attr.get_size()):
				expectedSent = attr.get_sentiment_num(i)
				if polarity * expectedSent >= 0:
					word = attr.get_word(i)
					significance = attr.get_weight_num(i)
					attrScore += bagOfWords.count(word) * significance
			
			attrWeight = attr.get_attr_weight_num()
			score += attrScore * attrWeight
			
		#print scores, text.encode('utf8')
		return score	