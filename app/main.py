from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
import time
from dotenv import load_dotenv
from typing import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.routers import auth_route
from app.dependencies import get_current_email
from app.routers import websocket_route

# Load .env file
load_dotenv()

app = FastAPI()

app.include_router(auth_route.router, prefix="/auth", tags=["auth"])
app.include_router(websocket_route.router, prefix="/websocket", tags=["websocket"])

templates = Jinja2Templates(directory="./frontend/public/pages")

app.mount("/public", StaticFiles(directory="./frontend/public"), name="public")
app.mount("/src", StaticFiles(directory="./frontend/src"), name="src")

origins = [
    "http://localhost:8080",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def root():
    # return {"mesage": "Hello World"}
    return RedirectResponse("/home")

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})

@app.get("/home")
async def home_page(request: Request):
    return templates.TemplateResponse(name="new_home.html", context={"request": request})
