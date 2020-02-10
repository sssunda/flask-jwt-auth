from flask import Flask, session
from apps.models.database import init_db, init_create_user
from apps.auth.views import auth, api


def create_app():
    app = Flask(__name__)
    init_db()
    # create test_user
    # init_create_user()
    api.init_app(auth)
    app.register_blueprint(auth, url_prefix='/auth')
    app.secret_key = 'super secret key'


    @app.route("/")
    def hello():
        return "Hello, World!"

    return app
