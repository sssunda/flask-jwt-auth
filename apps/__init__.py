# Third Party Module Import
from flask import Flask, Blueprint

# Apps Module Import
from apps.account.views import api
from apps.account.auth.views import ns_auth
from apps.account.users.views import ns_users
from apps.models.database import init_db, init_create_user

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("./configs/config.py")

    with app.app_context():
        init_db()
    # create test_user
    # init_create_user()

    blueprint = Blueprint('apps', __name__, url_prefix='')
    api.init_app(blueprint)
    api.add_namespace(ns_auth)
    api.add_namespace(ns_users)
    app.register_blueprint(blueprint)

    return app
