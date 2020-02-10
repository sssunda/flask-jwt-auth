from flask import Flask, session
from apps.models.database import init_db, init_create_user
from apps.account.views import api
from apps.account.auth.views import auth
from apps.account.users.views import users

def create_app():
    app = Flask(__name__)
    init_db()
    # create test_user
    # init_create_user()
    api.init_app(auth)
    api.init_app(users)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(users, url_prefix='/users')
    app.secret_key = 'super secret key'


    @app.route("/")
    def hello():
        return "Hello, World!"

    return app
