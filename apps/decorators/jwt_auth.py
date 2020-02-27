# Third Party Module Import
from flask import request, jsonify, make_response

# Python Module Import
from functools import wraps
import jwt
import time
import logging

# Apps Module Import
from apps.jwt.views import decrypt_jwt
from apps.models.database import get_session
from apps.models.user import User
from apps.utils.response import fail_response
from apps.utils.status_code import ERROR_UNAUTHORIZED


def jwt_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token is None:
            return fail_response("Token is not given")
        try:
            decoded_token = decrypt_jwt(token)
        except Exception as e:
            logging.error(e)
            return fail_response("Invalid token given", ERROR_UNAUTHORIZED)

        db = get_session('flask-jwt-auth')
        username = decoded_token['username']

        auth_user = db.query(User).filter_by(username=username).first()
        if auth_user is None:
            return fail_response("Invalid token given", ERROR_UNAUTHORIZED)

        exp = decoded_token['exp']
        if exp < time.time():
            return fail_response('Access token has been expired', ERROR_UNAUTHORIZED)

        kwargs['jwt_username'] = username
        kwargs['jwt_exp'] = exp
        kwargs['jwt_iat'] = decoded_token['iat']
        kwargs['auth_user'] = auth_user

        return f(*args, **kwargs)
    return decorated_function
