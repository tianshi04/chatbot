from datetime import datetime, timedelta, timezone
import os
import jwt
from dotenv import load_dotenv
from itsdangerous  import URLSafeTimedSerializer

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRATION = os.getenv("ACCESS_TOKEN_EXPIRATION", 60)
serializer = URLSafeTimedSerializer(SECRET_KEY)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRATION))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_onetimetoken(email: str):
    token = serializer.dumps(email, salt=SECRET_KEY)
    return token