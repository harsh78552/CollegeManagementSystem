from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from DATABASE.LIBRARY.bookDatabase import BookDatabase

blp = Blueprint('see book', __name__, description='')


@blp.route('/book-detail')
class BookDetails(MethodView):
	def __init__(self):
		self.book_db = BookDatabase()

	@jwt_required()
	def get(self):
		response = self.book_db.getAllBook()
		return response


@blp.route('/get-genre')
class BookGenre(MethodView):
	def __init__(self):
		self.book_db = BookDatabase()

	@jwt_required()
	def get(self):
		response = self.book_db.getGenre()
		return response


@blp.route('/get-book-genre')
class GetBook(MethodView):
	def __init__(self):
		self.book_db = BookDatabase()

	@jwt_required()
	def post(self):
		data = request.get_json()
		genre = data['genre']
		response = self.book_db.getGenreBook(genre)
		return response
