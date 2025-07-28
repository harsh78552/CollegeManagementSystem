from pymongo import MongoClient
from datetime import date


class FacultyNotificationDatabase:
	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client['CollegeSystem']
		self.collection = self.db['facultyNotifications']

	def insertNotification(self, message):
		message['date'] = str(date.today())
		self.collection.insert_one(message)
		return {'message': "notification sent successfully."}
