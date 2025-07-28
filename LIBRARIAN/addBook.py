from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from RoleBaseAuthenticator import chekRole
from DATABASE.LIBRARY.bookDatabase import BookDatabase
from flask_jwt_extended import jwt_required

blp = Blueprint('add book', __name__, description='book add system')


@blp.route('/upload-book')
class UploadBook(MethodView):
	def __init__(self):
		self.book_db = BookDatabase()

	@jwt_required()
	@chekRole('librarian')
	def post(self):
		data = request.get_json()
		response = self.book_db.insertBook(data['name'].title(), data['author'], data['publisher'],
		                                   data['published_year'],
		                                   data['edition'], data['genre'], data['total_copies'],
		                                   data['available_copies'], data['description'], data['location'])
		return response
