'''
Bark assistant 

A voice assistant interface for the Bark LLM moel.

Demonstrating a first-in-kind implementation of voice assistants 
on top of the Bark AI model.
'''

import os, datetime, time, json, io, pandas, uvicorn, random, jwt
from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request, status, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm, OAuth2PasswordBearer
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

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 60 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']   
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']   

# Auth
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

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
@app.post("/api/user/register", 
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
def register(payload: schemas.CreateUser, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email ==  payload.email).first()
    if user:
        raise HTTPException(status_code=403, detail="User already exists.")
    # create user 
    message, is_valid = helpers.email_is_valid(payload.email)
    if payload.password == payload.confirm_password:
        if is_valid:
            pw_hash=helpers.generate_password_hash(payload.password)
            db_user = models.User(email=payload.email, 
                                  password_hash=pw_hash,
                                  user_id=helpers.uuid4(),
                                  reset_id=helpers.uuid4(),
                                  create_date=helpers.get_date())

            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            # send email to confirm with a link
            response=schemas.CreateUserResponse(message="Successfully created user; confirm user account via email.",
                                                user_id=db_user.user_id)
            return response
        else:
            raise HTTPException(status_code=401, detail=message)
    else:
        HTTPException(status_code=401, detail="Passwords do not match.")

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
    access_token = helpers.create_access_token(user.email, ALGORITHM, JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = helpers.create_refresh_token(user.email, ALGORITHM, JWT_REFRESH_SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES)
    response=schemas.LoginResponse(access_token=access_token, refresh_token=refresh_token, expires=datetime.datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return response

# jwt protected route
@app.get("/api/user/details",
    responses={
        200: {"model": schemas.User},
        401: {
            "model": schemas.HTTPError,
            "description": "Token expired",
        },
        403: {
            "model": schemas.HTTPError,
            "description": "Could not validate credential",
        },
        404: {
            "model": schemas.HTTPError,
            "description": "User not found",
        },
    }, 
    tags=["users"], 
    status_code=200)
def get_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    token_payload=helpers.token_decode(token, JWT_SECRET_KEY, ALGORITHM)
    user = db.query(models.User).filter_by(email=token_payload['sub']).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return user

# session create
@app.post("/api/session/create",
    responses={
        201: {"model": schemas.Session},
        401: {
            "model": schemas.HTTPError,
            "description": "Token expired",
        },
        403: {
            "model": schemas.HTTPError,
            "description": "Could not validate credential",
        },
        404: {
            "model": schemas.HTTPError,
            "description": "User not found",
        },
    }, 
    tags=["sessions"], 
    status_code=201)
def session_create(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    token_payload=helpers.token_decode(token, JWT_SECRET_KEY, ALGORITHM)
    user = db.query(models.User).filter_by(email=token_payload['sub']).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    session=models.Session(id=helpers.uuid4(),
                            user_id=user.user_id,
                            create_date=datetime.datetime.now())

    db.add(session)
    db.commit()
    return schemas.Session(id=session.id, user_id=session.user_id, create_date=session.create_date)

# session create
@app.post("/api/session/query/create",
    responses={
        201: {"model": schemas.Query},
        401: {
            "model": schemas.HTTPError,
            "description": "Token expired",
        },
        403: {
            "model": schemas.HTTPError,
            "description": "Could not validate credential",
        },
        404: {
            "model": schemas.HTTPError,
            "description": "User not found",
        },
    }, 
    tags=["sessions"], 
    status_code=201)
def query_sample_create(payload: schemas.CreateQuery, file: UploadFile, token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    token_payload=helpers.token_decode(token, JWT_SECRET_KEY, ALGORITHM)
    user = db.query(models.User).filter_by(email=token_payload['sub']).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    session=db.query(models.Session).filter_by(session_id=payload.session_id).first()

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find session",
        )     

    query=models.Query(id=helpers.uuid4(),
                        session_id=payload.session_id,
                        user_id=user.user_id,
                        create_date=datetime.datetime.now(),
                        bucket="queries")
    db.add(query)
    db.commit()

    return schemas.Query(id=query.id, session_id=query.session_id, user_id=query.user_id, create_date=query.create_date, bucket=query.bucket)
    
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