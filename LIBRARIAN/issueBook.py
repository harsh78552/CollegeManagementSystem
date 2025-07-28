from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from DATABASE.LIBRARY.bookDatabase import BookDatabase
from DATABASE.LIBRARY.IssuedBookData import IssuedBookDatabase
from DATABASE.STUDENT.StudentDatabase import StudentDatabase
from datetime import timedelta, date, datetime

blp = Blueprint('book issue', __name__)


@blp.route('/issue-book')
class BookIssue(MethodView):
	def __init__(self):
		self.student_db = StudentDatabase()
		self.book_db = BookDatabase()
		self.issuedBook_db = IssuedBookDatabase()

	def post(self):
		data = request.get_json()
		registerationNo = data['regNo']
		bookName = data['bookName'].title()
		genre = data['genre']
		studentResponse = self.student_db.SearchStudent(registerationNo)
		if studentResponse:
			bookResponse = self.book_db.getBook(genre, bookName)
			bookResponse['available_copies'] = int(bookResponse['available_copies'])
			if bookResponse['available_copies'] > 0:
				bookResponse['available_copies'] -= 1
				try:
					self.book_db.updateBook(bookResponse)
					response = self.issuedBook_db.insertIssuedBookData(registerationNo, studentResponse['name'],
					                                                   bookName,
					                                                   datetime.combine(date.today(),
					                                                                    datetime.min.time()),
					                                                   date.today() + timedelta(days=15),
					                                                   )
					return response
				except Exception as error:
					return {'error': str(error)}, 503
			else:
				return {'message': 'All available copies of this book have been issued.'}, 400
		else:
			return {'message': 'Student not found. Please register first.'}, 404
