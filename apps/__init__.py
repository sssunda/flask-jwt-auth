# Third Party Module Import
from flask import Flask, Blueprint

# Apps Module Import
from apps.models.database import init_db, init_create_user
from apps.account.views import api
from apps.account.auth.views import ns_auth
from apps.account.users.views import ns_users
from apps.utils.get_config import get_config

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('configs.config')
    init_db()
    # create test_user
    # init_create_user()

    blueprint = Blueprint('apps', __name__, url_prefix='')
    api.init_app(blueprint)
    api.add_namespace(ns_auth)
    api.add_namespace(ns_users)
    app.register_blueprint(blueprint)

    secret_key = get_config('APP_SECRET_KEY')
    app.secret_key = secret_key

    return app
