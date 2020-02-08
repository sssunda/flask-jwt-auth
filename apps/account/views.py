from flask import Flask, Blueprint, session, redirect, url_for
from flask_restful import Resource, Api, reqparse
from models.user import User
from models.database import get_session
from datetime import datetime

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
            db = get_session('flask-jwt-auth')
            data = db.query(User).filter_by(username=args['username']).first()
            if data is not None:
                if data.check_password(args['password']):
                    session['logged_in'] = True
                    try:
                        db.query(User).filter_by(username=args['username']).update({'last_login': datetime.now()})
                        db.commit()
                    except:
                        db.rollback()
                return redirect(url_for('hello'))
        except Exception as e:
            return {'error': str(e)}


api.add_resource(Login,'/login')