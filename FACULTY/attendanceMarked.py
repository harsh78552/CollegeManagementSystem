from flask import request
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from RoleBaseAuthenticator import chekRole
from flask.views import MethodView
from DATABASE.STUDENT.StudentDatabase import StudentDatabase
from DATABASE.STUDENT.studentAttendanceDatabase import StudentAttendance

blp = Blueprint('student-name', __name__, description='student name come from backend')


@blp.route('/student-name')
class StudentName(MethodView):
	def __init__(self):
		self.student_db = StudentDatabase()

	@jwt_required()
	@chekRole('faculty')
	def post(self):
		data_ = self.student_db.fetch_all_student()
		print(data_)
		return data_


@blp.route('/submit-attendance')
class CollectAttendanceData(MethodView):
	def __init__(self):
		self.student_db = StudentAttendance()

	@jwt_required()
	def post(self):
		data = request.get_json()
		# print(data)
		response = self.student_db.insertStudentAttendance(data)
		return response
