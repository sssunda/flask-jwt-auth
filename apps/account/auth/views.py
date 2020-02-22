from flask_restplus import Resource, reqparse
from apps.models.user import User
from apps.models.database import get_session
from apps.jwt.views import encrypt_jwt
from apps.decorators.jwt_auth import jwt_token_required
from apps.account.views import api, login_parser
from datetime import datetime
from apps.utils.response import success_response, fail_response


ns_auth = api.namespace('auth')


@ns_auth.route('/login')
class Login(Resource):
    def post(self):
        parser = login_parser
        args = parser.parse_args()

        try:
            db = get_session('flask-jwt-auth')
            data = db.query(User).filter_by(username=args['username']).first()
            if data is not None:
                if data.check_password(args['password']):
                    access_token = encrypt_jwt(args['username'])
                    try:
                        db.query(User).filter_by(username=args['username']).update({'last_login': datetime.now()})
                        db.commit()
                    except:
                        db.rollback()
                    return success_response({'access_token': access_token})
        except Exception as e:
            return {'error': str(e)}


@ns_auth.route('/me')
class Me(Resource):
    @jwt_token_required
    def get(self, **kwargs):
        auth_user = kwargs['auth_user']
        data = {
            'id' : auth_user.id,
            'username' : auth_user.username,
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