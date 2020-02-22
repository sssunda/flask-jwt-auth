from flask import jsonify, make_response
from flask_restplus import Resource
from apps.decorators.jwt_auth import jwt_token_required
from apps.account.views import create_parser, update_parser
from apps.models.user import User
from apps.models.database import get_session
from apps.utils.validate import check_username, check_password, check_email
from apps.account.views import api

ns_users = api.namespace("users")

@ns_users.route('')
class Home(Resource):
    @jwt_token_required
    def get(self, **kwargs):
        auth_user = kwargs['auth_user']
        if not auth_user.is_staff:
            return make_response(jsonify({
                'msg': 'Not Permission. Only Staff'
            }), 401)
        db = get_session('flask-jwt-auth')
        user_list = db.query(User).all()

        data = list()
        for user in user_list:
            data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_on': user.created_on,
                'last_login': user.last_login,
                'is_staff': user.is_staff
            })
        return make_response(jsonify({
                'msg': 'success',
                'data': data
        }), 200)
    def post(self):
        parser = create_parser
        args = parser.parse_args()

        try:
            db = get_session('flask-jwt-auth')
            if db.query(User).filter_by(username=args['username']).first():
                return make_response(jsonify({
                    'msg': 'Already existed username'
                }), 401)
            
            if db.query(User).filter_by(email=args['email']).first():
                return make_response(jsonify({
                    'msg': 'Already existed email'
                }), 401)

            is_valid, err_msg = check_username(args['username'])
            if not is_valid:
                return make_response(jsonify({
                    'msg': err_msg
                }), 401)

            is_valid, err_msg = check_password(args['password'], args['password_confirmed'])
            if not is_valid:
                return make_response(jsonify({
                    'msg': err_msg
                }), 401)

            is_valid, err_msg = check_email(args['email'])
            if not is_valid:
                return make_response(jsonify({
                    'msg': err_msg
                }), 401)

            user = User(
                username=args['username'],
                password=args['password'],
                email=args['email']
            )
            db.add(user)
            print('add')
        except Exception as e:
            print(e)
            return db.rollback()

        db.commit()
        new_user = db.query(User).filter_by(username=args['username']).first()
        data = {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'created_on': new_user.created_on
            }
        return make_response(jsonify({
            'msg': 'success',
            'data': data
        }), 200)

@ns_users.route('/<username>')
class Username(Resource):
    @jwt_token_required
    def get(self, username, **kwargs):
        auth_user = kwargs['auth_user']
        if auth_user.is_staff or kwargs['jwt_username'] == username:
            db = get_session('flask-jwt-auth')
            user = db.query(User).filter_by(username=username).first()

            if user:
                auth_user = user
                data = {
                    'id': auth_user.id,
                    'username': auth_user.username,
                    'email': auth_user.email,
                    'created_on': auth_user.created_on,
                    'last_login': auth_user.last_login
                }
                return make_response(jsonify({
                    'msg': 'success',
                    'data': data
                }), 200)
            else:
                return make_response(jsonify({
                    'msg': 'No entry for username.{}'.format(username)
                }), 401)
        return make_response(jsonify({
            'msg': 'Not Permission'
        }), 401)

    @jwt_token_required
    def put(self, username, **kwargs):
        auth_user = kwargs['auth_user']
        parser = update_parser
        args = parser.parse_args()
        if kwargs['jwt_username'] == username or auth_user.is_staff:
            try:
                db = get_session('flask-jwt-auth')
                user = db.query(User).filter_by(username=username).first()

                is_valid, err_msg = check_password(args['password'], args['password_confirmed'])
                if not is_valid:
                    return make_response(jsonify({
                        'msg': err_msg
                    }), 401)

                is_valid, err_msg = check_email(args['email'])
                if not is_valid:
                    return make_response(jsonify({
                        'msg': err_msg
                    }), 401)

                user.set_password(args['password'])
                user.email = args['email']
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
                return make_response(jsonify({
                    'msg': 'Error while update user info'
                }), 401)
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_on': user.created_on,
                'last_login': user.last_login
            }
            return make_response(jsonify({
                'msg': 'success',
                'data': data
            }), 200)
        return make_response(jsonify({
            'msg': 'Not Permission'
        }), 401)

    @jwt_token_required
    def delete(self, username, **kwargs):
        auth_user = kwargs['auth_user']

        if kwargs['jwt_username'] == username or auth_user.is_staff:
            try:
                db = get_session('flask-jwt-auth')
                db.query(User).filter_by(username=username).delete()
                db.commit()
            except:
                db.rollback()
                return make_response(jsonify({
                    'msg': 'Error while deleting user {}'.format(username)
                }), 401)

            return make_response(jsonify({
                'msg': 'success. delete uesr {}'.format(username)
            }), 200)

        return make_response(jsonify({
            'msg': 'Not Permission'
        }), 401)