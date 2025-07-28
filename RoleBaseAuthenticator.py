from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt


def chekRole(*role_required):
    def decorator(x):
        @wraps(x)
        @jwt_required()
        def decorated_functions(*args, **kwargs):
            claims = get_jwt()
            if claims['role'] not in role_required:
                return jsonify({'message': 'Access denied. '}), 403
            return x(*args, **kwargs)

        return decorated_functions

    return decorator
