from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from DATABASE.FACULTY.facultyDatabase import FacultyDatabase
from DATABASE.STUDENT.StudentDatabase import StudentDatabase
from RoleBaseAuthenticator import chekRole

blp = Blueprint('HomePage', __name__, description='HomePage API')


@blp.route('/faculty-name')
class FetchFacultyName(MethodView):
	def __init__(self):
		self.faculty_db = FacultyDatabase()

	@chekRole('admin','student')
	def get(self):
		response = self.faculty_db.getAllFaculty()
		return response
