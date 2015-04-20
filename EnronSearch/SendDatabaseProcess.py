import multiprocessing


class SendDatabaseProcess(multiprocessing.Process):

	def __init__(self, db, scored_sentences_pipe):
		multiprocessing.Process.__init__(self)
		self.db = db
		self.scored_sentences_pipe = scored_sentences_pipe

	def run(self):
		self.send_sentences()

	def send_sentences(self):
		(score, sentence, user, word) = self.scored_sentences_pipe.get()
		self.db.add_post(user, 'Enron', sentence, word, score)

	def raise_exc(self, type):
		raise type