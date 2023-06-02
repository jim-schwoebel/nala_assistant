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
import datetime, jwt, shutil
from datetime import timedelta 
from typing import Union, Any

# for db queries 
import models
from email_validator import validate_email, EmailNotValidError

from transformers import WhisperProcessor, WhisperForConditionalGeneration, SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan, pipeline
import numpy as np
import soundfile as sf 
import os, json, datetime
from datasets import load_dataset
import torch
from datasets import load_dataset
import numpy as np 
from python_speech_features import mfcc
from python_speech_features import logfbank
from python_speech_features import ssc
import scipy.io.wavfile as wav

# load model and processor into memory
processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")

# speaker embeddings (loaded - so you don't need to do this each time)
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
tts_processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
tts_model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
tts_vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
mname = "facebook/blenderbot-400M-distill"
blender_model = BlenderbotForConditionalGeneration.from_pretrained(mname)
blender_tokenizer = BlenderbotTokenizer.from_pretrained(mname)

# import dolly
# https://huggingface.co/databricks/dolly-v2-12b (large)
# https://huggingface.co/databricks/dolly-v2-3b (small)
dolly_model = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")

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

def str_to_uuid(uuid_str):
	return uuid.UUID(uuid_str)

# Helper functions
def create_access_token(user_id: str, session_id: str, subject: Union[str, Any], ALGORITHM: str, JWT_SECRET_KEY: str, minutes: int = None) -> str:
	expires = datetime.datetime.utcnow() + timedelta(minutes=minutes)
	to_encode = {"exp": expires, "sub": str(subject), "user_id": user_id, "session_id": session_id}
	encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
	return encoded_jwt

def create_refresh_token(user_id: str, session_id: str, subject: Union[str, Any], ALGORITHM: str, JWT_REFRESH_SECRET_KEY: str, minutes: int = None) -> str:
	expires = datetime.datetime.utcnow() + timedelta(minutes=minutes)
	to_encode = {"exp": expires, "sub": str(subject),"user_id": user_id, "session_id": session_id}
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
	temp_audio_file='temp_'+audio_file
	os.system('ffmpeg -y -i %s -ac 1 -ar 16000 %s'%(audio_file, temp_audio_file))

	# keep temp file (16000 Hz mono)
	os.remove(audio_file)
	os.rename(temp_audio_file, audio_file)

	# read contents of temporary audio file
	audio_input, samplerate = sf.read(audio_file)
	audio_duration=len(audio_input)/samplerate

	# remove temporary audio file
	input_features = processor(audio_input, sampling_rate=samplerate, return_tensors="pt").input_features 

	# master operation json schema
	now_=datetime.datetime.now()
	transcription=''
	# generate token ids
	predicted_ids = model.generate(input_features)
	# decode token ids to text
	transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

	return transcription

def get_labels(vector, label, label2):
	sample_list=list()
	for i in range(len(vector)):
		sample_list.append(label+str(i+1)+'_'+label2)

	return sample_list
	
def audio_featurize(file: str):
	# from https://github.com/jim-schwoebel/allie/blob/master/features/audio_features/pspeech_features.py
	(rate,sig) = wav.read(file)
	mfcc_feat = mfcc(sig,rate)
	fbank_feat = logfbank(sig,rate)
	ssc_feat=ssc(sig, rate)

	one_=np.mean(mfcc_feat, axis=0)
	one=get_labels(one_, 'mfcc_', 'means')
	two_=np.std(mfcc_feat, axis=0)
	two=get_labels(one_, 'mfcc_', 'stds')
	three_=np.amax(mfcc_feat, axis=0)
	three=get_labels(one_, 'mfcc_', 'max')
	four_=np.amin(mfcc_feat, axis=0)
	four=get_labels(one_, 'mfcc_', 'min')
	five_=np.median(mfcc_feat, axis=0)
	five=get_labels(one_, 'mfcc_', 'medians')

	six_=np.mean(fbank_feat, axis=0)
	six=get_labels(six_, 'fbank_', 'means')
	seven_=np.mean(fbank_feat, axis=0)
	seven=get_labels(six_, 'fbank_', 'stds')
	eight_=np.mean(fbank_feat, axis=0)
	eight=get_labels(six_, 'fbank_', 'max')
	nine_=np.mean(fbank_feat, axis=0)
	nine=get_labels(six_, 'fbank_', 'min')
	ten_=np.mean(fbank_feat, axis=0)
	ten=get_labels(six_, 'fbank_', 'medians')

	eleven_=np.mean(ssc_feat, axis=0)
	eleven=get_labels(eleven_, 'spectral_centroid_', 'means')
	twelve_=np.mean(ssc_feat, axis=0)
	twelve=get_labels(eleven_, 'spectral_centroid_', 'stds')
	thirteen_=np.mean(ssc_feat, axis=0)
	thirteen=get_labels(eleven_, 'spectral_centroid_', 'max')
	fourteen_=np.mean(ssc_feat, axis=0)
	fourteen=get_labels(eleven_, 'spectral_centroid_', 'min')
	fifteen_=np.mean(ssc_feat, axis=0)
	fifteen=get_labels(eleven_, 'spectral_centroid_', 'medians')

	labels=one+two+three+four+five+six+seven+eight+nine+ten+eleven+twelve+thirteen+fourteen+fifteen
	features=np.append(one_,two_)
	features=np.append(features, three_)
	features=np.append(features, four_)
	features=np.append(features, five_)
	features=np.append(features, six_)
	features=np.append(features, seven_)
	features=np.append(features, eight_)
	features=np.append(features, nine_)
	features=np.append(features, ten_)
	features=np.append(features, eleven_)
	features=np.append(features, twelve_)
	features=np.append(features, thirteen_)
	features=np.append(features, fourteen_)
	features=np.append(features, fifteen_)

	return json.dumps(dict(zip(labels,features)))

def query_response(transcript: str, response_type: str, blender_model=blender_model, blender_tokenizer=blender_tokenizer, dolly_model=dolly_model) -> str:
	'''transcript --LLM--> question
			--> response limit (200 tokens)''' 
	# Q&A task --> info
	# ordering pizza --> action 
	if response_type == 'blender':
		# api call
		UTTERANCE = transcript
		inputs = blender_tokenizer([UTTERANCE], return_tensors="pt")
		reply_ids = blender_model.generate(**inputs)
		response=blender_tokenizer.batch_decode(reply_ids)[0]
	elif response_type == 'dolly':
		res = dolly_model(transcript)
		response=res[0]["generated_text"]
	else:
		response=transcript 
	print(response)
	return response

def cleanup_audio():
	'''
	take in audio files and move them all into the 'queries' folder after a query.
	'''
	listdir=os.listdir()
	curdir=os.getcwd()
	for file in listdir:
		if file.endswith('.wav'):
			shutil.move(curdir+'/'+file, curdir+'/queries/'+file)

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