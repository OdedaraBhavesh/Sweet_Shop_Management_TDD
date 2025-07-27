import jwt
from datetime import datetime, timedelta

SECRET_KEY = "kataTheSweetSpotIncubyte987"


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token if decoded_token["exp"] >= datetime.utcnow().timestamp() else None
    except:
        return None
