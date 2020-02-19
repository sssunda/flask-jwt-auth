import json
from apps.test.conftest import client

test_config = {
    'DB_URL':'sqlite:///flask-jwt-auth.db'
}
test_user = {
    'username': "test_user_1",
    'password': "test"
}

def test_login(client):
    # test login
    resp = client.post("/auth/login", json=test_user)
    assert resp.status_code == 200

    # check access_token
    access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    assert access_token


def test_me(client):
    # test login and get access_token
    resp = client.post("/auth/login", json=test_user)
    access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    assert access_token

    # test me
    resp = client.get('/auth/me', headers={
        "Authorization": access_token
    })
    assert resp.status_code == 200

    # test me not given access_token
    resp = client.get('/auth/me')
    assert resp.status_code == 401


def test_refresh(client):
    # test login and get access_token
    resp = client.post("/auth/login", json=test_user)
    access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    assert access_token

    # test refresh
    resp = client.get('/auth/refresh', headers={
        "Authorization": access_token
    })
    assert resp.status_code == 200

    new_access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    assert new_access_token

    # access_toekn compare with new_access_token
    assert access_token != new_access_token

    # test refresh not given access_token
    resp = client.get('auth/refresh')
    assert resp.status_code == 401