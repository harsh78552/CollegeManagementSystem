from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from DATABASE.FACULTY.notification import FacultyNotificationDatabase
from DATABASE.STUDENT.notification import StudentNotificationDatabase

blp = Blueprint('notification', __name__, description='notification api')


@blp.route('/send-notification')
class AdminNotification(MethodView):
	def __init__(self):
		self.faculty_db = FacultyNotificationDatabase()
		self.student_db = StudentNotificationDatabase()

	def post(self):
		data = request.get_json()
		if data['recipient'] == 'faculty':
			response = self.faculty_db.insertNotification(data)
			return jsonify(response)
		response = self.student_db.insertNotification(data)
		return jsonify(response)
