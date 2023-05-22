'''
Master place to write any helper functions for use in the main code base.

Helps to clean up the code base a little bit ;-)
'''
from werkzeug.security import generate_password_hash, check_password_hash
import uuid, datetime, secrets, os, requests, simplejson, smtplib, json, validators
from sqlalchemy import desc
from uuid import UUID
import pandas as pd
from datetime import timedelta 

# for db queries 
import models
from email_validator import validate_email, EmailNotValidError

########################################
##            DB Helpers              ##
########################################
'''
Helpers related to querying data from the database.
'''
def url_is_valid(url):
    if type(url) is str:
        validation = validators.url(url)
        if validation:
            return True
        else:
            return False 
    else:
        return False

def email_is_valid(email):
    try:
      # Check that the email address is valid.
      validation = validate_email(email, check_deliverability=False)
      email = validation.email
      message = "email is valid"
      return message, True 
    except EmailNotValidError as e:
      message=str(e)
      return message, False 

# hashing functions for users/passwords
def hash_password(password: str) -> str:
    return generate_password_hash(password)
    
def verify_password(password_hash: str, password: str):
    return check_password_hash(password_hash, password)

def uuid4() -> str:
    return str(uuid.uuid4())

def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.
    
     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}
    
     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.
    
     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """
    
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


# Helper functions
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

########################################
##       Main back-end functions      ##
########################################
def transcribe_audio(audio_file) -> str:
    transcript=''
    return transcript 

def query_chatgpt4(audio_file) -> str:
    query=''
    return query

def query_bark(transcript) -> str:
    query=''
    return query