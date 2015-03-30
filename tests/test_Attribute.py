import unittest
from Attribute import Attribute #CHANGETHIS

class test_Attribute(unittest.TestCase):
	def setUp(self):
		self.test = Attribute("test", 1, ["tests"], [1], [-1])

#__init__
	#pass
	def test000_000_init_blank(self):
		a = Attribute()
		correct = Attribute(name = "Attribute", attrWeight = 1,
			words = None, weights = None, sentiments = None)
		self.assertEquals(a, correct)
		
	def test000_001_init_notBlank(self):
		a = Attribute("test", 2, ["test"], [1], [3])
		self.assertEquals(a.name, "test")
		self.assertEquals(a.attrWeight, 2)
		self.assertEquals(a.words, ["test"])
		self.assertEquals(a.weights, [1])
		self.assertEquals(a.sentiments, [3])
		
#__eq__
	def test100_000_eq(self):
		one = Attribute("test", 2, ["test"], [1], [1])
		two = Attribute("test", 2, ["test"], [1], [1])
		self.assertEquals(one, two)
		
	def test100_001_eq_noteq_name(self):
		one = Attribute("test", 2, ["test"], [1], [1])
		two = Attribute("test1", 2, ["test"], [1], [1])
		self.assertNotEquals(one, two)
		
	def test100_002_eq_noteq_weight(self):
		one = Attribute("test", 2, ["test"], [1], [1])
		two = Attribute("test", 3, ["test"], [1], [1])
		self.assertNotEquals(one, two)
		
	def test100_003_eq_noteq_words(self):
		one = Attribute("test", 2, ["test"], [1], [1])
		two = Attribute("test", 2, ["test", "test2"], [1], [1])
		self.assertNotEquals(one, two)
		
	def test100_004_eq_noteq_weights(self):
		one = Attribute("test", 2, ["test"], [1], [1])
		two = Attribute("test", 2, ["test"], [1,2], [1])
		self.assertNotEquals(one, two)
		
	def test100_005_eq_noteq_sent(self):
		one = Attribute("test", 2, ["test"], [1], [3])
		two = Attribute("test", 2, ["test"], [1], [1, -1])
		self.assertNotEquals(one, two)
		
#set_name
	def test200_000_setname(self):
		self.test.set_name("realname")
		correct = Attribute("realname", 1, ["tests"], [1], [-1])
		self.assertEquals(self.test, correct)
		
#set_attr_weight
	def test300_000_setattrweight(self):
		self.test.set_attr_weight(3)
		correct = Attribute("test", 1, ["tests"], [1], [-1])
		self.assertEquals(self.test, correct)
		
#set_words
	def test400_000_setwords(self):
		self.test.set_words(["real", "words"])
		correct = Attribute("test",1, ["real", "words"], [1], [-1])
		self.assertEquals(self.test, correct)
		
#set_weight_nums
	def test500_000_setweights(self):
		self.test.set_weights(["High", "Low", "Blah", "Medium"])
		correct = Attribute("test", 1, ["tests"], [3,1,1,2], [-1])
		self.assertEquals(self.test, correct)
		
	def test500_001_setweights_blank(self):
		self.test.set_weights([])
		correct = Attribute("test", 1, ["tests"], [], [-1])
		self.assertEquals(self.test, correct)
		
#set_weights_nums
	def test600_000_setweightsnums(self):
		self.test.set_weights_nums([2,3])
		correct = Attribute("test", 1, ["tests"], [2,3], [-1])
		self.assertEquals(self.test, correct)
		
#set_sentiments
	def test700_000_setsents(self):
		self.test.set_sentiments(["Positive", "Neutral", "Negative"])
		correct = Attribute("test", 1, ["tests"], [1], [1, -1, -1])
		self.assertEquals(self.test, correct)
		
	def test700_001_setsents_blank(self):
		self.test.set_sentiments([])
		correct = Attribute("test", 1, ["tests"], [1], [])
		self.assertEquals(self.test, correct)
				
#set_sentiments_nums
	def test800_000_setsentsnums(self):
		self.test.set_sentiments_nums([-1, 0, 1])
		correct = Attribute("test", 1, ["tests"], [1], [-1, 0, 1])
		self.assertEquals(self.test, correct)
		
#getters (all together)
	#pass
	def test900_000_getword(self):
		self.assertEquals(self.test.get_word(0), "tests")
		
	def test900_001_getweight(self):
		self.assertEquals(self.test.get_weight(0), "Low")
		
	def test900_002_getweightnum(self):
		self.assertEquals(self.test.get_weight_num(0), 1)
		
	def test900_003_getsentiment(self):
		self.assertEquals(self.test.get_sentiment(0), "Negative")
		
	def test900_004_getsentiment(self):
		self.assertEquals(self.test.get_sentiment_num(0), -1)
		
	def test900_005_getsize(self):
		self.assertEquals(self.test.get_size(), 1)
		
	def test900_006_getsize_none(self):
		a = Attribute()
		self.assertEquals(a.get_size(), 0)
		
	def test900_007_getname(self):
		self.assertEquals(self.test.get_name(), "test")
		
	def test900_008_getattrweight(self):
		self.assertEquals(self.test.get_attr_weight(), 1)
		
	def test900_009_getwords(self):
		self.assertEquals(self.test.get_words(), ["tests"])
		
	def test900_010_getwords_none(self):
		a = Attribute()
		self.assertIsNone(a.get_words())
		
	def test900_011_getweights(self):
		self.assertEquals(self.test.get_weights(), [1])
		
	def test900_012_getweights_none(self):
		a = Attribute()
		self.assertIsNone(a.get_words)
		
	def test900_013_getsentiments(self):
		self.assertEquals(self.test.get_sentiments(), [-1])
		
	def test900_014_getsentiments_none(self):
		a = Attribute()
		self.assertIsNone(a.get_sentiments())
		
	def test900_015_getmaxscore(self):
		self.assertEquals(self.test.get_max_score(), 1)
		
	#fail
	def test900_900_getword_badindex(self):
		correctError = "get_word: "
		try:
			self.test.get_name(10000)
			self.fail("Error: no error!")
		except ValueError, e:
			self.assertEqual(correctError, str(e)[:len(correctError)])
		except Exception, e:
			self.fail(str(e))
			
	def test900_901_getweight_badindex(self):
		correctError = "get_word: "
		try:
			self.test.get_weight(10000)
			self.fail("Error: no error!")
		except ValueError, e:
			self.assertEqual(correctError, str(e)[:len(correctError)])
		except Exception, e:
			self.fail(str(e))
				
	def test900_902_getweightnum_badindex(self):
		correctError = "get_word: "
		try:
			self.test.get_weight_num(10000)
			self.fail("Error: no error!")
		except ValueError, e:
			self.assertEqual(correctError, str(e)[:len(correctError)])
		except Exception, e:
			self.fail(str(e))
			
	def test900_903_getsentiment_badindex(self):
		correctError = "get_word: "
		try:
			self.test.get_sentiment(10000)
			self.fail("Error: no error!")
		except ValueError, e:
			self.assertEqual(correctError, str(e)[:len(correctError)])
		except Exception, e:
			self.fail(str(e))
			
	def test900_904_getsentimentnum_badindex(self):
		correctError = "get_word: "
		try:
			self.test.get_sentiment_num(10000)
			self.fail("Error: no error!")
		except ValueError, e:
			self.assertEqual(correctError, str(e)[:len(correctError)])
		except Exception, e:
			self.fail(str(e))
			
	def test900_905_getmaxscore_noweights(self):
		correctError = "get_word: "
		try:
			a = Attribute()
			self.test.get_max_score()
			self.fail("Error: no error!")
		except ValueError, e:
			self.assertEqual(correctError, str(e)[:len(correctError)])
		except Exception, e:
			self.fail(str(e))
			
if __name__ == '__main__':
	unittest.main()  
	
