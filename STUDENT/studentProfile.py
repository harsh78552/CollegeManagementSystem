from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from DATABASE.STUDENT.StudentDatabase import StudentDatabase
from flask_jwt_extended import get_jwt_identity, jwt_required

blp = Blueprint('student-profile', __name__, description='grasp student data..')


@blp.route('/student-profile')
class StudentProfile(MethodView):
	def __init__(self):
		self.student_db = StudentDatabase()

	@jwt_required()
	def get(self):
		identity = get_jwt_identity()
		response = self.student_db.searchStudent(identity)
		return jsonify(response)
