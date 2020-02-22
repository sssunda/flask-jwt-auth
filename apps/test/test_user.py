import pytest
import tempfile
import json
from apps.test.conftest import client


test_user_success_one = {
    'username': 'testuser',
    'password': 'testtest',
    'password_confirmed': 'testtest',
    'email': 'testuser@test.com'
    }

test_user_success_two = {
    'username': 'testuser2',
    'password': 'testtest',
    'password_confirmed': 'testtest',
    'email': 'testuser2@test.com'
}

test_uesr_fail = {
    'username': 'TestUser',
    'password': 'testtest',
    'password_confirmed': 'testtes',
    'email': 'testuserfailtwo@test.com'
}

test_staff_user = {
    'username': 'test_user_1',
    'password': 'test'
}

test_is_not_staff_user = {
    'username': 'test_user_2',
    'password': 'test'
}


def test_create_delete(client):
    # test create user
    # test delete user

    resp = client.post("/users", json=test_user_success_one)
    assert resp.status_code == 200

    resp = client.post("/users", json=test_user_success_two)
    assert resp.status_code == 200

    resp = client.post("/users", json=test_uesr_fail)
    assert resp.status_code == 401

    resp = client.post("/auth/login", json=test_user_success_one)
    access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    resp = client.delete("/users/" + test_user_success_one['username'],
                         headers={'Authorization': access_token})
    assert resp.status_code == 200

    resp = client.delete("/users/" + test_user_success_one['username'],
                         headers={'Authorization': access_token})
    assert resp.status_code == 401


def test_get_userinfo(client):
    # test get user info

    resp = client.post("/auth/login", json=test_staff_user)
    access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    resp = client.get("/users", headers={
        "Authorization": access_token
    })
    assert resp.status_code == 200

    resp = client.post("/auth/login", json=test_is_not_staff_user)
    access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    resp = client.get("/users", headers={
        "Authorization": access_token
    })
    assert resp.status_code == 401

    resp = client.post("/auth/login", json=test_staff_user)
    access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    resp = client.get("/users/" + test_staff_user['username'],
                      headers={'Authorization': access_token})
    assert resp.status_code == 200


def test_update_userinfo(client):
    # test update user info

    test_user_success_two['password'] = 'testuser'
    test_user_success_two['password_confirmed'] = 'testuser'
    test_user_success_two['email'] = 'testsuccessuser@test.com'

    resp = client.post("/auth/login", json=test_staff_user)
    access_token = json.loads(resp.data.decode("utf-8"))['access_token']
    resp = client.put("/users/" + test_user_success_two['username'],
                      headers={'Authorization': access_token},
                      json=test_user_success_two)
    assert resp.status_code == 200

    test_user_success_two['password_confirmed'] = 'test'
    resp = client.put("/users/" + test_user_success_two['username'],
                      headers={'Authorization': access_token},
                      json=test_user_success_two)
    assert resp.status_code == 401

    # after test update user info, delete test_user_success_two
    resp = client.delete("/users/" + test_user_success_two['username'],
                         headers={'Authorization': access_token})
    assert resp.status_code == 200