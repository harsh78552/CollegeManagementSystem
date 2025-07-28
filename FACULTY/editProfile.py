from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from DATABASE.FACULTY.facultyDatabase import FacultyDatabase

blp = Blueprint("faculty update profile", __name__, description='student update profile api')


@blp.route('/faculty-update')
class FacultyUpdateProfile(MethodView):
	def __init__(self):
		self.faculty_db = FacultyDatabase()

	def put(self):
		data = request.get_json()
		updated_data = {'contact': data.get('contact'),
		                'subject': data.get('subject'),
		                'qualification': data.get('qualification'),
		                'blood_group': data.get('blood_group')
		                }
		response = self.faculty_db.EditProfile(data['email'], updated_data)
		return response
