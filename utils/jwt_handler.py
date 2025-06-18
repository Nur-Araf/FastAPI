from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
if REFRESH_SECRET_KEY is None:
    raise ValueError("REFRESH_SECRET_KEY environment variable is not set")
VERIFY_SECRET_KEY = os.getenv("VERIFY_SECRET_KEY")
if VERIFY_SECRET_KEY is None:
    raise ValueError("VERIFY_SECRET_KEY environment variable is not set")
ALGORITHM = "HS256"

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    VERIFY_TOKEN_EXPIRE_HOURS = int(os.getenv("VERIFY_TOKEN_EXPIRE_HOURS", 24))
except ValueError:
    raise ValueError("Token expiration times must be integers")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM) # type: ignore

def create_verify_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=VERIFY_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire, "type": "verify"})
    return jwt.encode(to_encode, VERIFY_SECRET_KEY, algorithm=ALGORITHM) # type: ignore

def decode_token(token: str, is_refresh: bool = False):
    key = REFRESH_SECRET_KEY if is_refresh else SECRET_KEY
    if key is None:
        raise ValueError("JWT secret key is not set")
    try:
        payload = jwt.decode(token, key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
