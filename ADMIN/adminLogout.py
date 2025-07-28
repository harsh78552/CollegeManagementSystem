from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt
from flask_smorest import Blueprint
from ADMIN.Blocklist import BLOCKLIST

blp = Blueprint("admin-logout", __name__, description='admin logout here')


@blp.route('/admin-logout')
class studentLogout(MethodView):
	@jwt_required()
	def post(self):
		jti = get_jwt()['jti']
		BLOCKLIST.add(jti)
		response = jsonify({"message": "logout successfully..."})
		unset_jwt_cookies(response)
		return response, 200
