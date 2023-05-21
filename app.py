'''
Bark assistant 

A voice assistant interface for the Bark LLM moel.

Demonstrating a first-in-kind implementation of voice assistants 
on top of the Bark AI model.
'''

import os, datetime, time, json, io, pandas, uvicorn, random
from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, or_
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from datetime import timedelta

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
    openapi_tags=tags_metadata,
    docs_url=None, 
    redoc_url=None
)

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

# audio routes for openAI -> Bark
	# fastapi 
	# minio
	# auth0
	# sqlite database

# front-end routes
#############################
# / 
	# main page
# user routes
@app.get("/", response_class=HTMLResponse, 
                  tags=["templates"], 
                  status_code=200, 
                  include_in_schema=False)
def home_page(request: Request, db: Session = Depends(get_db)):
    '''
        Home page.
    '''
    request.session["base_url"] = "/"
    request.session['nowtime'] = datetime.datetime.now().year
    return templates.TemplateResponse("audio_wake.html", {"request": request})

# /docs 
	# docs
# /login
	# logging in
# /logout
	# logging out (session.clear())
# /register
	# register account
# /bark
	# stream

# back-end routes 
#############################
# user registration (auth0)
	# /api/login
		# input
			# json {username: str, password: str}
		# output 
			# login token
	# /api/register
		# input
			# json {username: str, password: str, confirm_password: str}
		# output
			# json {"token": str, "expires": str}, 201

# main routes
	# /api/audio/query (minio /upload)
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