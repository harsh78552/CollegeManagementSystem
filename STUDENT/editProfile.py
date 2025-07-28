from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from DATABASE.STUDENT.StudentDatabase import StudentDatabase

blp = Blueprint("student update profile", __name__, description='student update profile api.')


@blp.route('/student-update')
class UpdateProfile(MethodView):
	def __init__(self):
		self.student_db = StudentDatabase()

	def put(self):
		data = request.get_json()
		updated_data = {'contact': data.get('contact'),
		                'year': data.get('year'),
		                'semester': data.get('semester'),
		                'address': data.get('address'),
		                'blood_group': data.get('blood_group')
		                }
		response = self.student_db.update_profile(data['email'], updated_data)
		return response
