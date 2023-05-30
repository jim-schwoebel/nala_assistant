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
	first_name = Column(String(128))
	last_name = Column(String(128))
	language = Column(String(20), default='en-us')
	last_update = Column(DateTime)

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

class Integration(Base):
	__tablename__ = 'integrations'
	integration_id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	create_date = Column(DateTime)
	name = Column(String(128))
	credentials = Column(String(2048))