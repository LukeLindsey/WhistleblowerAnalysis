import multiprocessing


class ScoreSentencesProcess(multiprocessing.Process):

	def __init__(self, scorer, matched_sentences_pipe, scored_sentences_pipe):
		multiprocessing.Process.__init__(self)
		self.matched_sentences_pipe = matched_sentences_pipe
		self.scored_sentences_pipe = scored_sentences_pipe
		self.scorer = scorer

	def run(self):
		self.score_sentences()

	def score_sentences(self):
		(sentence, word, user) = self.matched_sentences_pipe.recv()
		score = float(self.scorer.score(sentence))
		if score > 0:
			self.scored_sentences_pipe.send([score, sentence.replace("'", "''"), user, word])

	def raise_exc(self, type):
		raise type