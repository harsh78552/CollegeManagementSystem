from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from DATABASE.LIBRARY.bookDatabase import BookDatabase

blp = Blueprint("update book data", __name__)


@blp.route('/update-book-detail')
class UpdateBook(MethodView):
	def __init__(self):
		self.book_db = BookDatabase()

	def put(self):
		data = request.get_json()
		response = self.book_db.updateBook(data)
		return response
