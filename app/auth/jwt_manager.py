import datetime
import jwt
from app.config import SECRET_KEY

def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
