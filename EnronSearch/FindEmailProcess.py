import multiprocessing
import emailformat as ef
import os


class FindEmailProcess(multiprocessing.Process):

	def __init__(self, folder_location, formatted_emails_pipe, db):
		multiprocessing.Process.__init__(self)
		self.folder_location = folder_location + '/'
		self.formatted_emails_pipe = formatted_emails_pipe
		self.db = db

	def run(self):
		self.find_emails()

	def find_emails(self):
		my_sent_folder = r'/sent/'#, r'/sent_items/']  # there are more sent folders than this, let's start small though

		user_directory_list = os.listdir(self.folder_location)

		for user_dir in user_directory_list:
			#for my_sent_folder in my_sent_folders:
			for sent_folder, no_directories, email_files in os.walk(self.folder_location + user_dir + my_sent_folder):
				for email_file_name in email_files:
					email_file = open((sent_folder + email_file_name), 'r')
					email = email_file.read()
					email_file.close()
					email = ef.format_email(email)
					self.formatted_emails_pipe.put((email, user_dir))
			print user_dir

			self.db.add_user(user_dir, 0, 'Enron')

	def raise_exc(self, type):
		raise type