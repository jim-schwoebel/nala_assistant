from datetime import date
import json
from pydantic import BaseModel, Json
from typing import Union, List
from uuid import UUID

################################################
##              DATABASE SCHEMAS              ##
################################################
class User(BaseModel):
    id: UUID
    user_id: str
    reset_id: Union[str, None] = None
    create_date: date

    # get information 
    email: str
    password_hash: str
    is_confirmed: bool = False

    # name information
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    language: Union[str, None] = 'en-us'
    last_update: date
    
    class Config:
        orm_mode = True

class Query(BaseModel):
    id: UUID
    create_date: date
    transcript: Union[str, None] = None
    bucket: str
    class Config:
        orm_mode = True

class Operation(BaseModel):
    id: UUID
    reference_query: UUID
    create_date: date
    type_: Union[str, None] = None
    class Config:
        orm_mode = True

################################################
##               OTHER SCHEMAS                ##
################################################

'''
A place for all other pydantic schemas.
'''

class HTTPError(BaseModel):
    detail: str
    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }

class Response_Message(BaseModel):
    message: str

# user logins 
class CreateUser(BaseModel):
    email: str
    password: str
    confirm_password: str

class CreateUserResponse(BaseModel):
    message: str
    user_id: str

class LoginUser(BaseModel):
    email: str
    password: str

# create api keys
class LoginToken(BaseModel):
    login_token: str
    expires: date

# token for requests
class ApiToken(BaseModel):
    token_id: str