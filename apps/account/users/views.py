from flask import Blueprint, jsonify
from flask_restful import Resource
from apps.decorators.jwt_auth import jwt_token_required
from apps.account.views import api, create_parser, update_parser
from apps.models.user import User
from apps.models.database import get_session
from apps.utils.validate import check_username, check_password, check_email


users = Blueprint('users', __name__)

class Home(Resource):
    @jwt_token_required
    def get(self, **kwargs):
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
        return jsonify({
                'msg': 'success',
                'data': data
        })
    def post(self):
        parser = create_parser
        args = parser.parse_args()

        try:
            db = get_session('flask-jwt-auth')
            if db.query(User).filter_by(username=args['username']).first():
                return jsonify({
                    'msg': 'Already existed username'
                })
            
            if db.query(User).filter_by(email=args['email']).first():
                return jsonify({
                    'msg': 'Already existed email'
                })

            is_valid, err_msg = check_username(args['username'])
            if not is_valid:
                return jsonify({
                    'msg': err_msg
                })

            is_valid, err_msg = check_password(args['password'], args['password_confirmed'])
            if not is_valid:
                return jsonify({
                    'msg': err_msg
                })

            is_valid, err_msg = check_email(args['email'])
            if not is_valid:
                return jsonify({
                    'msg': err_msg
                })

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
        return jsonify({
            'msg': 'success',
            'data': data
        })

class Username(Resource):
    @jwt_token_required
    def get(self, username, **kwargs):
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
            return jsonify({
                'msg': 'success',
                'data': data
            })
        else:
            return jsonify({
                'msg': 'No entry for username.{}'.format(username)
            })

    @jwt_token_required
    def put(self, username, **kwargs):
        parser = update_parser
        args = parser.parse_args()
        print(args)
        if kwargs['jwt_username'] != username:
            return jsonify({
                'msg': "Not your id"
            })
        try:
            db = get_session('flask-jwt-auth')
            user = db.query(User).filter_by(username=username).first()

            is_valid, err_msg = check_password(args['password'], args['password_confirmed'])
            if not is_valid:
                return jsonify({
                    'msg': err_msg
                })

            is_valid, err_msg = check_email(args['email'])
            if not is_valid:
                return jsonify({
                    'msg': err_msg
                })

            user.set_password(args['password'])
            user.email = args['email']
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            return jsonify({
                'msg': 'Error while update user info'
            })
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_on': user.created_on,
            'last_login': user.last_login
        }
        return jsonify({
            'msg': 'success',
            'data': data
        })

    @jwt_token_required
    def delete(self, username, **kwargs):
        try:
            db = get_session('flask-jwt-auth')
            db.query(User).filter_by(username=username).delete()
            db.commit()
        except:
            db.rollback()
            return jsonify({
                'msg': 'Error while deleting user {}'.format(username)
            })

        return jsonify({
            'msg': 'success. delete uesr {}'.format(username)
        })





api.add_resource(Home, '')
api.add_resource(Username, '/<username>')
