from flask import jsonify, request
from flask_smorest import Blueprint
from flask.views import MethodView
from DATABASE.FACULTY.facultyDatabase import FacultyDatabase
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity, jwt_required
from datetime import timedelta
import hashlib

blp = Blueprint('faculty-login', __name__, description='faculty login here.')


@blp.route('/faculty-login')
class FacultyLogin(MethodView):
    def __init__(self):
        self.faculty_db = FacultyDatabase()

    def post(self):
        facultyData = request.get_json()
        email = facultyData.get('email')
        password = facultyData.get('password')
        response = self.faculty_db.searchFacultyOrAdmin(email)
        if response:
            if response['password'] == hashlib.sha256(password.encode('utf-8')).hexdigest():
                if response['role'] == 'faculty':
                    access_token = create_access_token(identity=email, additional_claims=({'role': response['role']}),
                                                       expires_delta=timedelta(hours=10))
                    response_ = jsonify({"message": 'faculty login successfully.', 'access_token': access_token})
                    set_access_cookies(response_, access_token)
                    return response_, 200
                else:
                    return jsonify({'message': 'user not authorised.'}), 401
            else:
                return jsonify({'message': 'password incorrect.', 'status': 'failed'}), 401
        return jsonify({'message': 'user not exist...'}), 404
