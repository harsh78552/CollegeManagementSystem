from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from DATABASE.STUDENT.MarksUpload import AdminMarksUploadDatabase
from RoleBaseAuthenticator import chekRole

blp = Blueprint('student see result', __name__, description='student result api.')


@blp.route('/see-result')
class SeeResult(MethodView):
	def __init__(self):
		self.studentResult_db = AdminMarksUploadDatabase()

	@chekRole('student')
	def post(self):
		data = request.get_json()
		print(data)
		roll = data['roll']
		semester = data['semester']
		response = self.studentResult_db.fetchResultData(roll, semester)
		return response


