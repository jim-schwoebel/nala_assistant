from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Float
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import Date
from database import *
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from werkzeug.security import generate_password_hash, check_password_hash

'''
Separate file just for models to help maintain structure in database,
should align with schemas.py.
'''

class User(Base):
	__tablename__ = 'users'
	id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
	user_id=Column(String(128))
	reset_id=Column(String(128))
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

class Query(Base):
	__tablename__ = 'queries'
	id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
	create_date = Column(DateTime)
	transcript = Column(String(128))
	bucket = Column(String(128))
	
class Operation(Base):
	# query (hi.wav) -> transcribe (hi.wav / hi.json) -> bark_predict (hi.wav / hi.json)
	# hi.json has k/v pair 
	__tablename__ = 'operations'
	id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
	reference_query=Column(GUID)
	create_date = Column(DateTime)
	type_= Column(String(128))