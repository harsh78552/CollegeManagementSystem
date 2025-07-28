from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from RoleBaseAuthenticator import chekRole
from DATABASE.STUDENT.MarksUpload import AdminMarksUploadDatabase

blp = Blueprint('attendance upload', __name__, description='attendance upload api')


@blp.route('/send-result')
class MarksUpload(MethodView):
	def __init__(self):
		self.result_db = AdminMarksUploadDatabase()

	@jwt_required()
	@chekRole('admin')
	def post(self):
		data = request.get_json()
		response = self.result_db.insertMarksData(data['name'], data['roll'], data['semester'], data['batch'],
		                                          data['branch'], data['subjects'])
		return jsonify({'message': response})
