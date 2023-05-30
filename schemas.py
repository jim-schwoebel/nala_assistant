from datetime import date
import json
from pydantic import BaseModel, Json
from typing import Union, List
from uuid import UUID


################################################
##              DATABASE SCHEMAS              ##
################################################
class User(BaseModel):
    user_id: UUID
    reset_id: UUID
    create_date: date

    # get information 
    email: str
    password_hash: str
    is_confirmed: bool = False

    # name/language
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    language: Union[str, None] = 'en-us'
    
    # personalized settings
    last_update: Union[date, None] = None
    last_email: Union[date, None] = None
    last_login: Union[date, None] = None
    last_login_city: Union[str, None] = None
    last_login_state: Union[str, None] = None
    last_login_country: Union[str, None] = None
    last_login_ip: Union[str, None] = None
    login_number: int
    signup_ip: Union[str, None] = None
    image_link: Union[str, None] = None
    phone_number: Union[str, None] = None
    gender: Union[str, None] = None
    age: float

    # assistant default settings
    sound: Union[str, None] = None
    voice: Union[str, None] = None
    response_type: Union[str, None] = None

    class Config:
        orm_mode = True

class Session(BaseModel):
    session_id: UUID
    user_id: UUID
    create_date: date
    class Config:
        orm_mode = True

class Query(BaseModel):
    query_id: UUID
    session_id: UUID
    user_id: UUID
    create_date: date
    features: Union[str, None] = None
    transcript: Union[str, None] = None
    bucket: str
    rating: Union[int, None] = None
    response: Union[str, None] = None
    response_method: Union[str, None] = None
    language: Union[str, None] = None
    city: Union[str, None] = None
    state: Union[str, None] = None
    country: Union[str, None] = None
    class Config:
        orm_mode = True

class Integration(BaseModel):
    integration_id: UUID
    create_date: date
    name: Union[str, None] = None
    credentials: Union[str, None] = None
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
    user_id: UUID

class LoginUser(BaseModel):
    username: str
    password: str

# create api keys
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

# token for requests
class ApiToken(BaseModel):
    token_id: str

class QueryRate(BaseModel):
    query_id: UUID
    rating: Union[int, None]

class QueryRateString(BaseModel):
    query_id: str
    rating: int

class UpdateUser(BaseModel):
    first: Union[str, None]
    last: Union[str, None]
    language: str = 'en-us'
    sound: str
    voice: str
    response_type: str