from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
import time
from dotenv import load_dotenv
from typing import Annotated

from app.routers import auth_route
from app.dependencies import get_current_email

# Load .env file
load_dotenv()

app = FastAPI()

app.include_router(auth_route.router, prefix="/auth", tags=["auth"])

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
    return {"mesage": "Hello World"}
