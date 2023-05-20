'''
Master place to write any helper functions for use in the main code base.

Helps to clean up the code base a little bit ;-)
'''
from werkzeug.security import generate_password_hash, check_password_hash
import uuid, datetime, secrets, os, requests, simplejson, smtplib, json, validators
from sqlalchemy import desc
from uuid import UUID
import pandas as pd
 
# for db queries 
import models
from email_validator import validate_email, EmailNotValidError

########################################
##            DB Helpers              ##
########################################
'''
Helpers related to querying data from the database.
'''

def token_is_valid(request, db):
    token_id=request.session.get('token_id')
    token=db.query(models.Api_Key).filter(models.Api_Key.token_id == token_id).first()
    nowtime=datetime.datetime.now()
    if token and token.expiration_date > nowtime:
        return True, token
    else:
        token=None
        return False, token

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