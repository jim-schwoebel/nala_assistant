# Nala
Nala is a voice-assistant framework to quickly build and prototype voice assistants within the greater context of the emerging large-language-model (LLM) landscape. With Nala you can easily intgrate with state-of-the-art (SOTA) transcription like [Whisper API](), text-to-speech synthesis engines like Microsoft's [SpeechT5 model](https://huggingface.co/microsoft/speecht5_tts), and LLMs like [Dolly-v2-3b](https://huggingface.co/databricks/dolly-v2-3b) within a nice front-end - across any arbitrary wake word powered with the [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#javascript).

- New visual here - gif of system

Here are some key features for Developers:

- **Extensible Architecture:** Nala offers a flexible and modular, python-centric FastAPI architecture that allows developers to extend its functionality with ease. Integrate voice commands, natural language processing, and intelligent responses into your projects effortlessly.
- **Rapid LLM Integration:** With Nala's intuitive APIs and comprehensive documentation, integrating LLM-enriched voice capabilities into your projects is a breeze. Save development time and effort while providing a powerful voice interface for your users.
- **Multi-Platform Support:** Nala is designed to work seamlessly across various platforms and operating systems (e.g. Mac/Linux). Whether you're building web applications, mobile apps, or even IoT devices, Nala can be easily integrated into your technology stack.
- **Privacy and Security:** Nala prioritizes user privacy and data security. Rest assured that all voice interactions are handled with utmost care, ensuring the confidentiality and integrity of user information. Easily tune encryption settings to the needs of your terms of use and users.

Note that this is a version 2.0, web-enabled version of [a prior voice assistant app here](https://github.com/jim-schwoebel/nala).

## getting started

### mac 
Install basic dependencies:
```
sudo apt-get install ffmpeg
git clone git@github.com:jim-schwoebel/bark_assistant.git
cd bark_assistant
virtualenv env 
source env/bin/activate
pip3 install -r requirements.txt
pip3 install git+https://github.com/suno-ai/bark.git
```
Generate a secret key for `SESSION_SECRET`, `JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY` and environment vars using the following line of code 3 times (save this in `.env`)
```
python -c 'import secrets; print(secrets.token_hex())'
```
Also, you need a `WEB_URL` and `TERMS_URL` for your website and the terms of use, accordingly. These also are in the `.env` file. 

To open and edit .env file:
```
nano .env
```
Then run the app:
```
uvicorn app:app --reload
```

You will now be able to visit localhost (`http://127.0.0.1:8000`) to use appication.

### linux with GPU
Install basic dependencies:
```
sudo apt-get install ffmpeg
git clone git@github.com:jim-schwoebel/bark_assistant.git
cd bark_assistant
virtualenv env 
source env/bin/activate
pip3 install -r gpu_requirements.txt
pip3 install git+https://github.com/suno-ai/bark.git
```
Generate a secret key for `SESSION_SECRET`, `JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY` and environment vars using the following line of code 3 times (save this in `.env`)
```
python -c 'import secrets; print(secrets.token_hex())'
```
Also, you need a `WEB_URL` and `TERMS_URL` for your website and the terms of use, accordingly. These also are in the `.env` file. 

To open and edit .env file:
```
nano .env
```
Then run the app:
```
uvicorn app:app --reload
```

You will now be able to visit localhost (`http://127.0.0.1:8000`) to use appication.

Note that you will need at least [1 NVIDIA V100 GPU](https://www.vultr.com/products/cloud-gpu/nvidia-a100/) to have a seamless user experience with the Bark model and various LLMs [like Dolly](https://github.com/databrickslabs/dolly).

## deploying to server

Follow these instructions to deploy on a server.

1. buy a domain on namecheap.com.
2. get a vultr account / forward DNS to cloudflare from domain.
3. get a cert.pem and private.pem file on cloudflare for the server.
4. create a virtual machine on vultr or a similar platform, forward CNAME on cloudflare to IP address of host.
5. set up the server with at least 1 NVIDIA V100 GPU (e.g. `pip3 install -r gpu_requirements.txt`), as described in the `linux with GPU section` (getting started) above
6. run the command on the server with uvicorn below

Enable firewall rules for SSL (port 443)
```
sudo ufw allow 80
sudo ufw allow 443
```
```
nohup gunicorn --bind {ip_address}:443 main:app --certfile=cert.pem --keyfile=private.pem -w 10 --graceful-timeout 30 -t 30 --worker-class=uvicorn.workers.UvicornWorker --workers 10 </dev/null &>/dev/null &
```

`</dev/null &>/dev/null &` is a statement means that it is a background job, and you need to change [ip_address] with the right IP adddress.

## settings

Here are the current settings that you can edit in th `settings.json` file:
```json
{"website_name": "Nala",
    "wake_word": "hey", 
    "sounds": {"default": "chime", "options": ["chime", "bell"]}, 
    "voice": {"default": "bark", "options": ["microsoft", "bark"]}, 
    "response_type": {"default": "dolly", 
    "options": ["blender","dolly", "echo"]}, 
    "language": {"default": "en-us", "options": ["en-us"]}}
```

You can edit the website name, wakeword, sounds, voice, response_type, options, and language here in the file. Note that the options listed here are currently the only options provided in the repository, but they are easy-to-extend as a framework later in the `helpers.py` file.

## browser compatibility
Currently, Nala works on Chrome and Safari-based browsers based on [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#javascript) standards. If you load Nala on any other browser, it will give an error message like this.
![](https://github.com/jim-schwoebel/bark_assistant/blob/main/static/images/error.png)

## references 

### javascript front-end 
- [bootstrap icons](https://icons.getbootstrap.com/) - use bootstrap and bootstrap icons for javascript front-end
- [recorder.js](https://github.com/mattdiamond/Recorderjs) - to record audio files with bootstrap icon buttons
- [howlers.js](https://github.com/goldfire/howler.js) - playback audio for assistant
- [wavesurfer.js](https://wavesurfer-js.org/) - for enumerating last audio file generated in the browser
- [audio.js](http://kolber.github.io/audiojs/) - playback audio alternative (setting)
### feature extraction
- [python_speech_features](https://github.com/jim-schwoebel/allie/blob/master/features/audio_features/pspeech_features.py) - audio feature extraction method useed
- [audio_features - Allie](https://github.com/jim-schwoebel/allie/tree/master/features/audio_features)
### future tools used
- [minio](https://github.com/minio/minio) - minio is an object storage platform
- [auth0](https://github.com/auth0) - authentication
