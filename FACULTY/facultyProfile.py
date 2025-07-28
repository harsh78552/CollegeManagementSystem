from flask import request
from flask_smorest import Blueprint
from flask.views import MethodView
from DATABASE.FACULTY.facultyDatabase import FacultyDatabase

blp = Blueprint('faculty-profile', __name__, description='faculty profile api')


@blp.route('/faculty-profile')
class FacultyProfile(MethodView):
	def __init__(self):
		self.faculty_db = FacultyDatabase()

	def post(self):
		data = request.get_json()
		email = data['email']
		response = self.faculty_db.searchFacultyOrAdmin(email)
		return response
