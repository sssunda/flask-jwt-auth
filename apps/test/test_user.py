import pytest
import tempfile
import json
from apps.test.conftest import client


test_user_success = {
    'username': 'testuser',
    'password': 'test',
    'password_confirmed': 'test',
    'email': 'testuser@test.com'
    }
test_uesr_fail_one = {
    'username': 'test_user',
    'password': 'tes',
    'password_confirmed': 'test',
    'email': 'test@testm'
}
test_uesr_fail_two = {
    'username': 'TestUser',
    'password': 'testtest',
    'password_confirmed': 'testtes',
    'email': 'testuserfailtwo@test.com'
}

def test_create(client):
    # test create user

    # it can be just one time( Already create user )
    resp = client.post("/users", json=test_user_success)
    # assert resp.status_code == 200
    assert resp.status_code == 401

    resp = client.post("/users", json=test_uesr_fail_one)
    assert resp.status_code == 401


