import jwt
import time

# jwt setting
JWT_EXP_PERIOD = 3600
JWT_ALGO = "HS256"
JWT_SECRET_KEY = "super secret key"


def encrypt_jwt(username):
    iat = time.time()
    payload = {
        'username': username,
        'iat': iat,
        'exp': iat + JWT_EXP_PERIOD
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGO).decode("utf-8")


def decrypt_jwt(token):
    return jwt.decode(token, JWT_SECRET_KEY, algorithm=JWT_ALGO)
