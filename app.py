'''
Bark assistant 

A voice assistant interface for the Bark LLM moel.

Demonstrating a first-in-kind implementation of voice assistants 
on top of the Bark AI model.
'''

import os, datetime, time, json, io, pandas, uvicorn, random, jwt
from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, or_
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from datetime import timedelta


# minio
from minio import Minio
from minio.error import S3Error

# auth0 
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request

# load environment vars in .env
load_dotenv()

# import schemas and database engine
import models, schemas, helpers
from database import *

# bind engine to database
models.Base.metadata.create_all(bind=engine)

# create api docs and app
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
]

app = FastAPI(
    # following the docs https://fastapi.tiangolo.com/tutorial/metadata/
    # advanced docs: https://fastapi.tiangolo.com/advanced/extending-openapi/
    title="Bark assistant app",
    description="Build a voice assistant with the Bark LLM model in <1 minute.",
    version="0.0.2",
    terms_of_service="http://example.com/terms/",
    contact={"url": "https://barkassistant.com"},
    openapi_tags=tags_metadata)

app.add_middleware(SessionMiddleware, secret_key=os.getenv('SESSION_SECRET'))
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# add https redirect middleware for routing to https
# app.add_middleware(HTTPSRedirectMiddleware)

# setup minio instance
minio_client = Minio(
    "your-minio-url",
    access_key="your-access-key",
    secret_key="your-secret-key",
    secure=False  # Set to True if your Minio server uses HTTPS
)

# setup auth0 instance
oauth = OAuth()
auth0 = oauth.register(
    'auth0',
    client_id='YOUR_AUTH0_CLIENT_ID',
    client_secret='YOUR_AUTH0_CLIENT_SECRET',
    api_base_url='https://YOUR_AUTH0_DOMAIN',
    access_token_url='https://YOUR_AUTH0_DOMAIN/oauth/token',
    authorize_url='https://YOUR_AUTH0_DOMAIN/authorize',
    client_kwargs={'scope': 'openid profile email'}
)

# jwt 
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_TOKEN_EXPIRE")

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# front-end routes
#############################
# /main page
# user routes
@app.get("/", response_class=HTMLResponse, 
                  tags=["templates"], 
                  status_code=200, 
                  include_in_schema=False)
def home(request: Request, db: Session = Depends(get_db)):
    '''
        Home page.
    '''
    request.session["base_url"] = "/"
    request.session['nowtime'] = datetime.datetime.now().year
    return templates.TemplateResponse("home.html", {"request": request})

# /login
	# logging in
@app.get("/login", response_class=HTMLResponse, 
                  tags=["templates"], 
                  status_code=200, 
                  include_in_schema=False)
def login(request: Request, db: Session = Depends(get_db)):
    '''
        Home page.
    '''
    return templates.TemplateResponse("login.html", {"request": request})

# /logout
	# logging out (session.clear())
@app.get("/logout", response_class=HTMLResponse, 
                  tags=["templates"], 
                  status_code=200, 
                  include_in_schema=False)
def logout(request: Request, db: Session = Depends(get_db)):
    '''
        Home page.
    '''
    return templates.TemplateResponse("logout.html", {"request": request})

# /register
	# register account
@app.get("/register", response_class=HTMLResponse, 
                  tags=["templates"], 
                  status_code=200, 
                  include_in_schema=False)
def register(request: Request, db: Session = Depends(get_db)):
    '''
        Home page.
    '''
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/reset", response_class=HTMLResponse, 
                  tags=["templates"], 
                  status_code=200, 
                  include_in_schema=False)
def reset(request: Request, db: Session = Depends(get_db)):
    '''
        Home page.
    '''
    return templates.TemplateResponse("reset.html", {"request": request})

# /bark
	# stream
@app.get("/bark", response_class=HTMLResponse, 
                  tags=["templates"], 
                  status_code=200, 
                  include_in_schema=False)
def bark_assistant(request: Request, db: Session = Depends(get_db)):
    '''
        Home page.
    '''
    request.session["base_url"] = "/"
    request.session['nowtime'] = datetime.datetime.now().year
    return templates.TemplateResponse("audio_wake.html", {"request": request})

# /docs 
    # docs


# back-end routes 
#############################
@app.post("/api/user/login", 
    responses={
        200: {"model": schemas.LoginResponse},
        401: {
            "model": schemas.HTTPError,
            "description": "Incorrect password for user",
        },
        404: {
            "model": schemas.HTTPError,
            "description": "User does not exist",
        },
    }, 
    tags=["users"], 
    status_code=200)
def login(payload: schemas.LoginUser, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email ==  payload.email).first()
    if helpers.verify_password(user.password_hash, payload.password):
        pass
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = helpers.create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    response=schemas.LoginResponse(access_token=access_token, token_type="bearer", expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return response

# @app.get("/api/protected",
#     responses={
#         200: {"model": schemas.LoginResponse},
#         401: {
#             "model": schemas.HTTPError,
#             "description": "Incorrect password for user",
#         },
#         404: {
#             "model": schemas.HTTPError,
#             "description": "User does not exist",
#         },
#     }, 
#     tags=["users"], 
#     status_code=200)
# def protected(credentials: HTTPAuthorizationCredentials = security):
#     try:
#         payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         user = db.query(models.User).filter(models.User.email ==  username).first()
#         if not user:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         return {"message": "Hello, {}! You accessed the protected route.".format(username)}
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token has expired")
#     except (jwt.DecodeError, jwt.InvalidTokenError):
#         raise HTTPException

# main routes
    # api/audio/upload (minio /upload)
        # input
            # audio file (blob)
            # json (metadata)
        # output 
            # json, code (201)

	# /api/audio/transcribe (minio /transcribe)
		# input
			# audio file (blob)
			# json (metadata)
		# output 
			# json, code (201)

	# /api/audio/generate (minio /generate)
		# input
			# audio file (blob)
			# json (metadata)
		# output 
			# audio file (blob)
			# json (metadata), 201