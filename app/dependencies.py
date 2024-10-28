from fastapi import Cookie, HTTPException, status
import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
from typing import Annotated

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_current_email(access_token: Annotated[str, Cookie()] = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        print("SECRET_KEY:", SECRET_KEY)
        print("ALGORITHM:", ALGORITHM)
        print("Access Token:", access_token)

        payload = jwt.decode(access_token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        exp = payload.get("exp")
        if exp is not None:
            expiration_date = datetime.fromtimestamp(exp, timezone.utc)
            if expiration_date < datetime.now(timezone.utc):
                raise credentials_exception
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT Error",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise credentials_exception
    
    return email