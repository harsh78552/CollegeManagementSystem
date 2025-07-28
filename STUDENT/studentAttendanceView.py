from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from DATABASE.STUDENT.studentAttendanceDatabase import StudentAttendance

blp = Blueprint('student-view-attendance', __name__, description='student view attendance api')


@blp.route('/student-view-attendance')
class StudentViewAttendance(MethodView):
	def __init__(self):
		self.attendance_db = StudentAttendance()

	@jwt_required()
	def post(self):
		email = get_jwt_identity()
		data = request.get_json()
		response = self.attendance_db.getAttendance(email, data['subject'], data['date'])
		if response:
			return jsonify(response)
		else:
			return jsonify({"message": 'attendance not marked..'})
