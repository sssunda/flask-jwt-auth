# Third Party Module Import
import jwt

# Python Module Import
import time

# Apps Module Import
from apps.utils.get_config import get_config



def encrypt_jwt(username):
    jwt_exp_period = get_config('JWT_EXP_PERIOD')
    jwt_algo = get_config('JWT_ALGO')
    jwt_secret_key = get_config('JWT_SECRET_KEY')

    iat = time.time()
    payload = {
        'username': username,
        'iat': iat,
        'exp': iat + jwt_exp_period
    }
    return jwt.encode(payload, jwt_secret_key, algorithm=jwt_algo).decode("utf-8")


def decrypt_jwt(token):
    jwt_algo = get_config('JWT_ALGO')
    jwt_secret_key = get_config('JWT_SECRET_KEY')
    return jwt.decode(token, jwt_secret_key, algorithm=jwt_algo)
