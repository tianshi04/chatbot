from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse
import os
from app.utils.token_utils import create_access_token
from dotenv import load_dotenv
import requests
from typing import Annotated

router = APIRouter()

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
scope = "email profile"

@router.get("/login")
def login_with_google():
    login_url = (
        "https://accounts.google.com/o/oauth2/auth?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"scope={scope}"
    )
    return RedirectResponse(login_url)

@router.get("/callback")
def google_callback(code: str, response: Response):
    try:
        token_response = requests.post(
        "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code"
            },
        )
        token_json = token_response.json()
        google_access_token = token_json.get("access_token")
        user_info_response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {google_access_token}"},
        )
        # TODO: Save user info to database
        access_token = create_access_token({ "sub": user_info_response.json().get("email") })
        response.set_cookie("access_token", access_token, httponly=True, samesite="Lax")
        return {"message": "Successfully logged in"}
    except Exception:
        return {"message": "Failed to log in"}

@router.get("/logout")
def logout(response: Response):
    response.set_cookie("access_token", "", expires=0)
    return {"message": "Đăng xuất thành công"}
