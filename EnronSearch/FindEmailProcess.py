import multiprocessing
import emailformat as ef
import os


class FindEmailProcess(multiprocessing.Process):

	def __init__(self, folder_location, formatted_emails_queue, usernames_queue, db):
		multiprocessing.Process.__init__(self)
		self.email_main_directory = folder_location + '/'
		self.formatted_emails_queue = formatted_emails_queue
		self.db = db
		self.usernames_queue = usernames_queue

	def run(self):
		self.find_emails()

	def find_emails(self):
		my_sent_folders = [r'/sent/', r'/sent_items/']  # there are more sent folders than this, let's start small though

		user_directory_list = os.listdir(self.email_main_directory)

		for user_dir in user_directory_list:
			for my_sent_folder in my_sent_folders:
				for sent_folder, no_directories, email_files in os.walk(self.email_main_directory + user_dir + my_sent_folder):
					for email_file_name in email_files:
						# The extra forward slash is in case there is another folder inside the sent folder.
						email_file = open((sent_folder + "/" + email_file_name), 'r')
						email = email_file.read()
						email_file.close()
						self.formatted_emails_queue.put([email, user_dir])
			print user_dir

			self.usernames_queue.put(user_dir)
			print "hello"
			#self.db.add_user(user_dir, 0, 'Enron')
