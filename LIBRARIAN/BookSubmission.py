from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from DATABASE.LIBRARY.IssuedBookData import IssuedBookDatabase
from DATABASE.LIBRARY.bookDatabase import BookDatabase
from datetime import date, timedelta

blp = Blueprint('book submission', __name__)


@blp.route('/submission-book')
class BookSubmit(MethodView):
	def __init__(self):
		self.student_db = IssuedBookDatabase()
		self.book_db = BookDatabase()

	def delete(self):
		data = request.get_json()
		registerationNo = data['regNo']
		bookName = data['bookName']
		genre = data['genre']
		studentResponse = self.student_db.getData(registerationNo, bookName)
		bookResponse = self.book_db.getBook(genre, bookName)
		day = studentResponse['submissionDate'].date() - date.today()
		day = day.days
		if day < 0:
			response = self.student_db.deleteStudentData(registerationNo, bookName)
			if response:
				bookResponse['available_copies'] += 1
				self.book_db.updateBook(bookResponse)
				return {'message': f'Due to late submission ₹{abs(day) * 1} need to pay.'}, 200
		else:
			response = self.student_db.deleteStudentData(registerationNo, bookName)
			if response:
				bookResponse['available_copies'] += 1
				self.book_db.updateBook(bookResponse)
				return response
