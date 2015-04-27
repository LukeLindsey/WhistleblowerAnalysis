import threading
import ctypes
import inspect


class SendSentencesThread(threading.Thread):

	def __init__(self, db, scored_sentences_queue):
		threading.Thread.__init__(self)
		self.db = db
		self.scored_sentences_queue = scored_sentences_queue

	def run(self):
		self.send_sentences()

	def send_sentences(self):
		try:
			(score, sentence, user, word) = self.scored_sentences_queue.get()
			print sentence
			#self.db.add_post(user, 'Enron', sentence, word, score)
		except KeyboardInterrupt:
			print('\n Enron: Terminated by user (send sentences)\n')

	def _get_my_tid(self):
		if not self.isAlive():
			raise threading.ThreadError("the thread is not active")

		# do we have it cached?
		if hasattr(self, "_thread_id"):
			return self._thread_id

		# no, look for it in the _active dict
		for tid, tobj in threading._active.items():
			if tobj is self:
				self._thread_id = tid
				return tid

		raise AssertionError("could not determine the thread's id")

	def raiseExc(self, exctype):
		self._async_raise(self._get_my_tid(), exctype)

	def _async_raise(self, tid, exctype):

		if not inspect.isclass(exctype):
			raise TypeError("Only types can be raised (not instances)")
		res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),
														 ctypes.py_object(exctype))
		if res == 0:
			raise ValueError("invalid thread id")
		elif res != 1:
			# "if it returns a number greater than one, you're in trouble,
			# and you should call it again with exc=NULL to revert the effect"
			ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
			raise SystemError("PyThreadState_SetAsyncExc failed")
