from fastapi import APIRouter, Response, Body, HTTPException
from fastapi.responses import RedirectResponse
import os
from app.models.google_token import GoogleToken
from app.utils.token_utils import create_access_token
from dotenv import load_dotenv
import requests
from typing import Annotated
from google.oauth2 import id_token
from google.auth.transport import requests as googleRequest

router = APIRouter()

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
scope = "email profile"

@router.get("/login")
async def login_with_google():
    login_url = (
        "https://accounts.google.com/o/oauth2/auth?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"scope={scope}"
    )
    return RedirectResponse(login_url)

@router.get("/callback")
async def google_callback(code: str, response: Response):
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
        # return {"message": "Successfully logged in"}
        redirect_url = "http://localhost:8000/home"
        response.headers["Location"] = redirect_url
        response.status_code = 302
        return response
    except Exception:
        return {"message": "Failed to log in"}

@router.post("/callback")
async def google_callback_from_web(respone: Response, token: Annotated[GoogleToken, Body()]):
    try:
        idinfo = id_token.verify_oauth2_token(token.token, googleRequest.Request(), CLIENT_ID)
        email = idinfo['email']
        access_token = create_access_token({ "sub": email })
        respone.set_cookie("access_token", access_token, httponly=True, samesite="Lax")
        return {"message": "Successfully logged in"}
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))
        

@router.get("/logout")
async def logout(response: Response):
    response.set_cookie("access_token", "", expires=0)
    return {"message": "Đăng xuất thành công"}
