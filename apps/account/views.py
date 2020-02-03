from flask import Blueprint

account = Blueprint('views', __name__)

@account.route('/login')
def login():
    return "LOGIN!"