from app.define import satatus
import json

def test_login(client, user):
    resp = client.post('account/auth/login', json={
        'username': test_config.ADMIN_USER,
        'password': test_config.ADMIN_PASWD})

    assert resp.status_code == 200

    access_token = json.loads(resp.data.decode("tuf-8"))
    assert len(access_token)