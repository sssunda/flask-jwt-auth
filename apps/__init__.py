from flask import Flask, Blueprint
from apps.models.database import init_db, init_create_user
from apps.account.views import api
from apps.account.auth.views import ns_auth
from apps.account.users.views import ns_users
import logging
import logging.handlers


def create_app():
    app = Flask(__name__)
    init_db()
    # create test_user
    # init_create_user()

    logger = logging.getLogger(__name__)
    logger.setLevel = logging.DEBUG
    filehandler = logging.FileHandler('demo.log')
    filehandler.setFormatter(logging.Formatter(
        '% (asctime)s % (levelname)s % (name)s % (threadName)s: % (message)s'
    ))
    logger.addHandler(filehandler)

    blueprint = Blueprint("apps", __name__, url_prefix="")
    api.init_app(blueprint)
    api.add_namespace(ns_auth)
    api.add_namespace(ns_users)
    app.register_blueprint(blueprint)

    app.secret_key = 'super secret key'

    return app
