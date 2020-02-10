from flask import Blueprint
from flask_restful import Resource
from apps.account.views import api


users = Blueprint('users', __name__)

class Home(Resource):
    def get(self):
        return {'success': 'success!'}

api.add_resource(Home, '')
