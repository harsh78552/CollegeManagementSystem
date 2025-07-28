from flask import request, jsonify
from flask_smorest import Blueprint
from flask_jwt_extended import set_access_cookies, create_access_token
from datetime import timedelta
from DATABASE.FACULTY.facultyDatabase import FacultyDatabase
from flask.views import MethodView
import hashlib

blp = Blueprint('admin-login_', __name__, description='admin login api')


@blp.route('/admin-login')
class AdminLogin(MethodView):
	def __init__(self):
		self.faculty_db = FacultyDatabase()

	def post(self):
		data = request.get_json()
		email = data['email']
		password = data['password']
		response = self.faculty_db.searchFacultyOrAdmin(email)
		if response:
			if response['email'] == email and response['password'] == hashlib.sha256(
					password.encode('utf-8')).hexdigest():
				if response['role'] == 'admin':
					access_token = create_access_token(identity=email, additional_claims=({'role': response['role']}),
					                                   expires_delta=timedelta(hours=8))
					response = jsonify({'message': 'admin login successfully.', 'access_token': access_token})
					set_access_cookies(response, access_token)
					return response, 200
				else:
					return jsonify({'message': 'user not authorised.'}), 401
			else:
				return jsonify({'message': 'wrong password'}), 401
		return jsonify({'message': 'user not found.'}), 404
