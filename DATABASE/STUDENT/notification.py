from pymongo import MongoClient
from datetime import date


class StudentNotificationDatabase:
	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client['CollegeSystem']
		self.collection = self.db['studentNotifications']

	def insertNotification(self, message):
		message['date'] = str(date.today())
		self.collection.insert_one(message)
		return {'message': "notification sent successfully.", 'date': date.today()}

	def getNotification(self):
		data = self.collection.find()
		notificationList = []
		for data_ in data:
			data_Dict = {'notification': data_['message'], 'date': data_['date']}
			notificationList.append(data_Dict)
		return notificationList


