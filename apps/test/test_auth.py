import pytest
import tempfile
import json
from apps.account.auth.views import Login
from apps import create_app
from apps.models.database import init_db

test_config = {
    'DB_URL':'sqlite:///flask-jwt-auth.db'
}
test_user = {
    'username': "test_user_1",
    'password': "test"
}

@pytest.fixture(scope='session')
def api():
    app = create_app()
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as api:
        with app.app_context():
            init_db()
        yield api


def test_login(api):
    # test login
    resp = api.post("/auth/login", json=test_user)
    assert resp.status_code == 200

    # check access_token
    access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    assert access_token


def test_me(api):
    # test login and get access_token
    resp = api.post("/auth/login", json=test_user)
    access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    assert access_token

    # test me
    resp = api.get('/auth/me', headers={
        "Authorization": access_token
    })
    assert resp.status_code == 200

    # test me not given access_token
    resp = api.get('/auth/me')
    assert resp.status_code == 401


def test_refresh(api):
    # test login and get access_token
    resp = api.post("/auth/login", json=test_user)
    access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    assert access_token

    # test refresh
    resp = api.get('/auth/refresh', headers={
        "Authorization": access_token
    })
    assert resp.status_code == 200

    new_access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    assert new_access_token

    # access_toekn compare with new_access_token
    assert access_token != new_access_token

    # test refresh not given access_token
    resp = api.get('auth/refresh')
    assert resp.status_code == 401