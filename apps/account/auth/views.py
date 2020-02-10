from flask import Blueprint, jsonify, make_response
from flask_restful import Resource, reqparse
from apps.models.user import User
from apps.models.database import get_session
from apps.jwt.views import encrypt_jwt
from apps.decorators.jwt_auth import jwt_token_required
from apps.account.views import api
from datetime import datetime


auth = Blueprint('auth', __name__)

class Login(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except Exception as e:
            return {'error': str(e)}
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
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
                    return make_response(jsonify({
                        'msg': 'Success!',
                        'access_token': access_token
                    }), 200)
        except Exception as e:
            return {'error': str(e)}

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
        return make_response(jsonify({
            'msg': 'Success!',
            'data': data
        }), 200)

class Refresh(Resource):
    @jwt_token_required
    def get(self, **kwargs):
        new_token = encrypt_jwt(kwargs['jwt_username'])
        print(new_token)
        return make_response(jsonify({
            'msg': 'Success!',
            'access_token': new_token
        }))

api.add_resource(Login, '/login')
api.add_resource(Me, '/me')
api.add_resource(Refresh, '/refresh')