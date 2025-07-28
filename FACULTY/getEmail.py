from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint("get email", __name__, description='get email api..')


@blp.route('/get-email')
class GetEmail(MethodView):
	@jwt_required()
	def get(self):
		email = get_jwt_identity()
		return jsonify({'email': email})
