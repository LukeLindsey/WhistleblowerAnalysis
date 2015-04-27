import multiprocessing
import Queue as QueueStandard


class ScoreSentencesProcess(multiprocessing.Process):

	def __init__(self, scorer, matched_sentences_queue, scored_sentences_queue):
		multiprocessing.Process.__init__(self)
		self.matched_sentences_queue = matched_sentences_queue
		self.scored_sentences_queue = scored_sentences_queue
		self.scorer = scorer

	def run(self):
		score = True
		while score:
			try:
				self.score_sentences()
			except QueueStandard.Empty:
				score = False
		print "DONE SCORING USERS"


	def score_sentences(self):
		(sentence, word, user) = self.matched_sentences_queue.get(True, 5)
		score = self.scorer.score(sentence)
		if score > 0:
			self.scored_sentences_queue.put([score, sentence.replace("'", "''"), user, word])

	def raise_exc(self, type):
		raise type