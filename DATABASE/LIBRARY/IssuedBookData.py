from datetime import datetime
from pymongo import MongoClient


class IssuedBookDatabase:
	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client['CollegeSystem']
		self.collection = self.db['issuedBooks']

	def insertIssuedBookData(self, registerationNo, studentName, bookName, issueDate, submissionDate):
		issuedBookData = {'registerationNo': registerationNo, 'studentName': studentName, 'bookName': bookName,
		                  'issueDate': issueDate, 'submissionDate': datetime.combine(
				submissionDate,
				datetime.min.time())}
		try:
			self.collection.insert_one(issuedBookData)
			return {'message': f'book submission date on {submissionDate}'}, 200
		except Exception as error:
			return {'message': str(error)}, 503

	def getData(self, registerationNo, bookName):
		response = self.collection.find()
		for studentData in response:
			if studentData['registerationNo'] == registerationNo and studentData[
				'bookName'] == bookName:
				studentData['_id'] = str(studentData['_id'])
				return studentData

	def deleteStudentData(self, registerationNo, bookName):
		response = self.collection.delete_one({'registerationNo': registerationNo, 'bookName': bookName})
		try:
			if response.deleted_count:
				return {'message': 'book submitted successfully'}, 200
		except Exception as error:
			return {'message': str(error)}, 503
