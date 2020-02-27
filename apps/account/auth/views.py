# Third Party Module Import
from flask_restplus import Resource, reqparse

# Python Module Import
from datetime import datetime
import logging

# Apps Module Import
from apps.models.user import User
from apps.models.database import get_session
from apps.jwt.views import encrypt_jwt
from apps.decorators.jwt_auth import jwt_token_required
from apps.account.views import api
from apps.utils.response import success_response, fail_response


ns_auth = api.namespace('auth')

# login parser
login_parser = reqparse.RequestParser()
login_parser.add_argument('username', required=True)
login_parser.add_argument('password', required=True)


@ns_auth.route('/login')
class Login(Resource):
    def post(self):
        try:
            args = login_parser.parse_args()
        except Exception as e:
            logging.error(e)
            return fail_response('Need Info : username, password')

        try:
            db = get_session()
            data = db.query(User).filter_by(username=args['username']).first()
            if data is not None:
                if data.check_password(args['password']):
                    access_token = encrypt_jwt(args['username'])
                    try:
                        db.query(User).filter_by(username=args['username']).update(
                            {'last_login': datetime.now()})
                        db.commit()
                    except Exception as e:
                        logging.error(e)
                        db.rollback()
                        return fail_response('Error while login')
                    return success_response({'access_token': access_token})
                return fail_response('Invalid password')
            return fail_response('Invalid user')
        except Exception as e:
            logging.error(e)
            return fail_response('Login error')


@ns_auth.route('/me')
class Me(Resource):
    @jwt_token_required
    def get(self, **kwargs):
        auth_user = kwargs['auth_user']
        data = {
            'id': auth_user.id,
            'username': auth_user.username,
            'email': auth_user.email,
            'created_on': auth_user.created_on,
            'token_iat': kwargs['jwt_iat'],
            'token_exp': kwargs['jwt_exp']
        }
        return success_response(data)


@ns_auth.route('/refresh')
class Refresh(Resource):
    @jwt_token_required
    def get(self, **kwargs):
        new_token = encrypt_jwt(kwargs['jwt_username'])
        return success_response({'access_token': new_token})
