from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Float
from sqlalchemy_utils import UUIDType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import Date
from database import *
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

'''
Separate file just for models to help maintain structure in database,
should align with schemas.py.
'''

class User(Base):
	__tablename__ = 'users'
	user_id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	reset_id= Column(UUIDType(binary=False))
	create_date = Column(DateTime)

	# get information 
	email = Column(String(128))
	password_hash = Column(String(128))
	is_confirmed = Column(Boolean, default=False)

	# name/language
	first_name = Column(String(128))
	last_name = Column(String(128))
	language = Column(String(20), default='en-us')
	
	# other user information
	last_update = Column(DateTime)
	last_email = Column(DateTime)
	last_login = Column(DateTime)
	last_login_city = Column(String(128))
	last_login_state = Column(String(128))
	last_login_country = Column(String(128))
	last_login_ip = Column(String(128))
	login_number = Column(Integer, default=0)
	signup_ip = Column(String(128))
	image_link = Column(String(256))
	phone_number = Column(String(128))
	gender = Column(String(128))
	age = Column(Float)

	# default_settings
	sound=Column(String(128))
	voice=Column(String(128))
	response_type=Column(String(128))
	
	# hashing functions for users/passwords
	def hash_password(self, password):
		self.password_hash = generate_password_hash(password)
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

class Session(Base):
	__tablename__ = 'sessions'
	session_id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	user_id = Column(UUIDType(binary=False))
	create_date = Column(DateTime)

class Query(Base):
	__tablename__ = 'queries'
	query_id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	session_id=Column(UUIDType(binary=False))
	user_id=Column(UUIDType(binary=False))
	create_date = Column(DateTime)
	features = Column(String(1028))
	transcript = Column(String(128))
	bucket = Column(String(128))
	rating = Column(Integer)
	response = Column(String(1028))
	response_method = Column(String(128))
	language = Column(String(20), default='en-us')
	city = Column(String(128))
	state = Column(String(128))
	country = Column(String(128))

class Integration(Base):
	__tablename__ = 'integrations'
	integration_id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	create_date = Column(DateTime)
	name = Column(String(128))
	credentials = Column(String(2048))