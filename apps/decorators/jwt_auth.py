from flask import request, jsonify, make_response
from functools import wraps
import jwt
import time
from apps.jwt.views import decrypt_jwt
from apps.models.database import get_session
from apps.models.user import User


def jwt_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token is None:
            return make_response(jsonify({
                'msg': "Token is not given",
            }), 401)
        try:
            decoded_token = decrypt_jwt(token)
        except Exception as e:
            print(e)
            return make_response(jsonify({
                'msg': "Invalid token given",
            }), 401)

        db = get_session('flask-jwt-auth')
        username = decoded_token['username']

        auth_user = db.query(User).filter_by(username=username).first()
        if auth_user is None:
            return make_response(jsonify({
                'msg': "Invalid token given",
            }), 401)

        exp = decoded_token['exp']
        if exp < time.time():
            return make_response(jsonify({
                'msg': "Access token has been expired",
            }), 401)

        kwargs['jwt_username'] = username
        kwargs['jwt_exp'] = exp
        kwargs['jwt_iat'] = decoded_token['iat']
        kwargs['auth_user'] = auth_user
        print(kwargs)


        return f(*args, **kwargs)
    return decorated_function