from flask import Blueprint, jsonify
from flask_restful import Resource
from apps.decorators.jwt_auth import jwt_token_required
from apps.account.views import api, create_parser
from apps.models.user import User
from apps.models.database import get_session

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
            user = User(
                username=args['username'],
                password=args['password'],
                email=args['email']
            )
            db.add(user)

        except Except as e:
            print(e)
            return db.rollback()

        db.commit()
        new_user = db.query(User).filter_by(username=args['username']).first()
        data = {
            'id' : new_user.id,
            'username' : new_user.username,
            'email': new_user.email,
            'created_on': new_user.created_on
            }
        return jsonify({
            'msg': 'success',
            'data': data
        })

api.add_resource(Home, '')
