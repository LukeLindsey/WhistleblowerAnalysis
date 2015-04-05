import unittest
from SearchPacket import SearchPacket
from SearchInterface import SearchInterface
from Attribute import Attribute
from GuiThread import GuiThread

class test_Tweet(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.interface = SearchInterface()
		attribute = Attribute("Test Attribute", attrWeight = 1,
			words = ['pizza'], weights = [3], sentiments = [1])
		self.attributes = [attribute]

	@classmethod
	def tearDownClass(self):
		self.interface.db.delete_keyspace()
		self.interface.db.close()
		

	def test_create_instance_with_valid_parameters(self):	
		thread = GuiThread(self.interface, self.attributes, {})
		self.assertIsInstance(thread, GuiThread)

	def test_create_instance_with_invalid_interface_parameter(self):
		try:
			thread = GuiThread("Invalid", self.attributes, {})
			self.fail()
		except TypeError:
			pass
	
	def test_create_instance_with_invalid_attributes_parameter(self):
		try:
			thread = GuiThread(self.interface, "Invalid", {})
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_invalid_args_parameter(self):
		try:
			thread = GuiThread(self.interface, self.attributes, "Invalid")
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_missing_interface_parameter(self):
		try:
			thread = GuiThread(attributes=self.attributes, args={})
			self.fail()
		except TypeError:
			pass
	
	def test_create_instance_with_missing_attributes_parameter(self):
		try:
			thread = GuiThread(interface=self.interface, args={})
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_missing_args_parameter(self):
		try:
			thread = GuiThread(interface=self.interface, attributes=self.attributes)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_empty_attributes_list(self):
		try:
			thread = GuiThread(interface=self.interface, attributes=[], args={})
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_attributes_list_containing_invalid_objects(self):
		try:
			thread = GuiThread(interface=self.interface, attributes=["Invalid"], args={})
			self.fail()
		except TypeError:
			pass

if __name__ == '__main__':
    unittest.main()

