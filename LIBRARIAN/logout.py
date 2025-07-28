from flask import request, jsonify
from flask_jwt_extended import get_jwt, unset_jwt_cookies, jwt_required
from flask.views import MethodView
from flask_smorest import Blueprint
from LIBRARIAN.blocklist import BLOCKLIST

blp = Blueprint('librarian logout', __name__, description='librarian logout system')


@blp.route('/librarian-logout')
class LibrarianLogout(MethodView):
	@jwt_required()
	def post(self):
		jti = get_jwt()['jti']
		BLOCKLIST.add(jti)
		response = jsonify({'message': 'logout successfully.'})
		unset_jwt_cookies(response)
		return response, 200
