'''
Master place to write any helper functions for use in the main code base.

Helps to clean up the code base a little bit ;-)
'''
from fastapi import HTTPException, status
from werkzeug.security import generate_password_hash, check_password_hash
import uuid, datetime, secrets, os, requests, simplejson, smtplib, json, validators
from sqlalchemy import desc
from uuid import UUID
import pandas as pd
import datetime, jwt
from datetime import timedelta 
from typing import Union, Any

# for db queries 
import models
from email_validator import validate_email, EmailNotValidError

# from transformers import WhisperProcessor, WhisperForConditionalGeneration, SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import numpy as np
import soundfile as sf 
import os, json, datetime
from datasets import load_dataset
import torch
from datasets import load_dataset

'''
# load model and processor into memory
processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")

# speaker embeddings (loaded - so you don't need to do this each time)
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
tts_processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
tts_model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
tts_vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
'''
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

def get_date():
    return datetime.datetime.now() 

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
def create_access_token(subject: Union[str, Any], ALGORITHM: str, JWT_SECRET_KEY: str, minutes: int = None) -> str:
    expires = datetime.datetime.utcnow() + timedelta(minutes=minutes)
    to_encode = {"exp": expires, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], ALGORITHM: str, JWT_REFRESH_SECRET_KEY: str, minutes: int = None) -> str:
    expires = datetime.datetime.utcnow() + timedelta(minutes=minutes)
    to_encode = {"exp": expires, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def token_decode(token: str, JWT_SECRET_KEY: str, ALGORITHM: str):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        if datetime.datetime.fromtimestamp(payload['exp']) < datetime.datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Could not validate credentials", 
                            headers={"WWW-Authenticate": "Bearer"})

    return payload

'''
## audio operations 
def tts_generate(text: str, filename: str, speaker_embeddings=speaker_embeddings, processor=tts_processor, model=tts_model, vocoder=tts_vocoder):
    # create tts prediction
    inputs = processor(text=text, return_tensors="pt")
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
    sf.write(filename, speech.numpy(), samplerate=16000)
    return filename


def audio_transcribe(audio_file: str, model=model, processor=processor):
    # set model configuration
    model.config.forced_decoder_ids = None
    
    # create temporary audio file
    temp_audiofile='temp_'+audio_file
    os.system('ffmpeg -y -i %s -ac 1 -ar 16000 %s'%(audio_file, temp_audiofile))

    # read contents of temporary audio file
    audio_input, samplerate = sf.read(temp_audiofile)
    audio_duration=len(audio_input)/samplerate

    # remove temporary audio file
    os.remove(temp_audiofile)
    input_features = processor(audio_input, sampling_rate=samplerate, return_tensors="pt").input_features 

    # master operation json schema
    now_=datetime.datetime.now()
    transcription=''
    # generate token ids
    predicted_ids = model.generate(input_features)
    # decode token ids to text
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

    return transcription
'''
########################################
##       Main back-end functions      ##
########################################
def send_email(to_: str, from_: str, subject: str):
    return subject

def transcribe_audio(audio_file: str) -> str:
    transcript=''
    return transcript 

def query_chatgpt4(audio_file: str) -> str:
    query=''
    return query

def query_bark(transcript: str) -> str:
    query=''
    return query