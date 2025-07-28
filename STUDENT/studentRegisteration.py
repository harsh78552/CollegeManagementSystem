from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from SCHEMA.STUDENT.StudentSchema import StudentRegisteration
from DATABASE.STUDENT.StudentDatabase import StudentDatabase

blp = Blueprint('student-registeration', __name__, description='student registered from here..')


@blp.route('/student-registration')
class UserRegister(MethodView):
	def __init__(self):
		self.student_db = StudentDatabase()

	@blp.arguments(StudentRegisteration)
	def post(self, request_data):
		name = request_data['name']
		contact = request_data['contact']
		email = request_data['email']
		password = request_data['password']
		branch = request_data['branch']
		registeration_no = request_data['registeration_no']
		year = request_data['year']
		semester = request_data['semester']
		blood_group = request_data['blood_group']
		address = request_data['address']
		sentResponse = self.student_db.insert_data(name, contact, email, password, branch, registeration_no, year,
		                                           semester, blood_group, address)
		return jsonify(sentResponse)
