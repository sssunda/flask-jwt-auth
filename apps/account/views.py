from flask import Flask, Blueprint
from flask_restful import Resource, Api, reqparse

account = Blueprint('views', __name__)
api = Api()


class Login(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except Exception as e:
            return {'error': str(e)}

api.add_resource(Login,'/login')