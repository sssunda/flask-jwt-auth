from flask import Flask, Blueprint, session, redirect, url_for
from flask_restful import Resource, Api, reqparse
from models.user import User

account = Blueprint('views', __name__)
api = Api()


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
            data = User.query.filter_by(username=args['username'], password=args['password']).first()
            if data is not None:
                session['logged_in'] = True

            return redirect(url_for('hello'))
        except Exception as e:
            return {'error': str(e)}


api.add_resource(Login,'/login')