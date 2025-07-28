from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from DATABASE.STUDENT.StudentDatabase import StudentDatabase
from flask_jwt_extended import create_access_token, set_access_cookies
from datetime import timedelta
import hashlib

blp = Blueprint('student--login', __name__, description='student login here.')


@blp.route('/student-login')
class StudentLogin(MethodView):
	def __init__(self):
		self.student_db = StudentDatabase()

	def post(self):
		student_data = request.get_json()
		email = student_data.get('email')
		password = student_data.get('password')
		response = self.student_db.searchStudent(email)
		if response:
			if response['password'] == hashlib.sha256(password.encode('utf-8')).hexdigest():
				access_token = create_access_token(identity=email, additional_claims=({'role': response['role']}),
				                                   expires_delta=timedelta(hours=5))
				response = jsonify({"message": 'student login successfully..', 'access_token': access_token})
				set_access_cookies(response, access_token)
				return response, 200
			return jsonify({'message': "incorrect password⚠️⚠️⚠️⚠️"}), 401
		return jsonify({'message': 'user not exist...'}), 404
