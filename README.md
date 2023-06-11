
<p align="center">
   <img src="https://camo.githubusercontent.com/eeee9b9732ef382762afd4a9dfd9a126c850e377fb51ad5cd2654a1d5768acb6/68747470733a2f2f6d656469612e67697068792e636f6d2f6d656469612f56447a5647386c764e527566752f67697068792e676966">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)]()
[![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/anfederico/Clairvoyant.svg)](https://github.com/jim-schwoebel/bark_assistant/issues)
[![License](https://img.shields.io/badge/license-Apache%202-blue)](https://www.apache.org/licenses/LICENSE-2.0.html)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)](https://github.com/users/jim-schwoebel/projects/2)

 </p>
 
# Nala
![](https://img.shields.io/github/stars/jim-schwoebel/bark_assistant?style=social) ![](https://img.shields.io/github/stars/jim-schwoebel/bark_assistant?label=Fork) ![](https://img.shields.io/youtube/views/:videoId)

Nala is a voice-assistant framework to quickly build and prototype voice assistants in <5 minutes within the greater context of the emerging large-language-model (LLM) landscape. With Nala you can easily intgrate with state-of-the-art (SOTA) transcription like [Whisper API](https://huggingface.co/docs/transformers/model_doc/whisper), text-to-speech synthesis engines like Microsoft's [SpeechT5 model](https://huggingface.co/microsoft/speecht5_tts), and LLMs like [Dolly-v2-3b](https://huggingface.co/databricks/dolly-v2-3b) within a nice front-end - across any arbitrary wake word powered with the [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#javascript).

![](https://github.com/jim-schwoebel/bark_assistant/blob/main/static/images/output.gif)

Here are some key features for Developers:

- **Extensible Architecture:** Nala offers a flexible and modular, python-centric FastAPI architecture that allows developers to extend its functionality with ease. Integrate new response models or TTS voice skins into your projects effortlessly.
- **Native LLM Integration:** Nala integrates directly with the the [Dolly-v2-3b](https://huggingface.co/databricks/dolly-v2-3b) LLM model - and makes it easy for you to integrate with others using an easy-to-follow strategy with helper functions.
- **Multi-Platform Support:** Nala is designed to work seamlessly across various platforms and operating systems (e.g. Mac/Linux and Chrome/Safari). Whether you're building web applications, mobile apps, or even IoT devices, Nala can be easily integrated into your technology stack.
- **Audio-to-Audio API**: Nala's FastAPI design allows for you to submit an audio file and get back audio file responses through the query-response model; few projects out there exist to help guide you through how to do this, so this may help accelerate learning for your voice assistant projects.
- **Simple UI**: Nala provides a simple user interface for users to quickly rate responses with thumbs up or thumbs-down to aid in building reinforcement learning models with [Reinforcement Learning with Human Feedback](https://medium.com/aiguys/reinforcement-learning-from-human-feedback-instructgpt-and-chatgpt-693d00cb9c58).
- **Privacy and Security:** Nala allows for downloads to be administered by superusers as specified in the `settings.json` - as well as authenticates users and sessions with standard JSON web tokens. Other features like encryption at rest, deletion of audio files, and other defaults are being worked on right now to preserve user privacy.

Note that this is a version 2.0, web-enabled version of [a prior voice assistant app here](https://github.com/jim-schwoebel/nala).

## getting started

### mac 
Install basic dependencies:
```
sudo apt-get install ffmpeg
git clone git@github.com:jim-schwoebel/nala_assistant.git
cd nala_assistant
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
Note if you having trouble with the `uvicorn app:app --reload` command, you can try:
```
python3 -m uvicorn app:app --reload
```

And sometimes this make it work.

You will now be able to visit localhost (`http://127.0.0.1:8000`) to use appication.

### linux with GPU
Install basic dependencies:
```
sudo apt-get install ffmpeg
git clone git@github.com:jim-schwoebel/nala_assistant.git
cd nala_assistant
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

### api docs
Once you have setup the app locally, you can get to the api docs @ `http://127.0.0.1:8000/docs` (for swagger docs) or `http://127.0.0.1:8000/redoc` (for redoc). The recommended set of docs to use is `http://127.0.0.1:8000/docs` (swagger) as there is greater support for authentication with JSON web tokens and audio-to-audio routes. A screenshot is shown below of the docs to give you an idea of what they look like. The auto-generated docs via FastAPI make it much easier to expand the routes to your particular need as a developer.

![](https://github.com/jim-schwoebel/nala_assistant/blob/main/static/images/docs.png)

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
    "super_users": ["jim@schwoebel.me"],
    "sounds": {"default": "chime", "options": ["chime", "bell"]}, 
    "voice": {"default": "bark", "options": ["microsoft", "bark"]}, 
    "response_type": {"default": "dolly", "options": ["blender","dolly", "echo"]}, 
    "language": {"default": "en-us", "options": ["en-us"]}}
```

You can edit the website name, wakeword, super_users (who can download data), sounds (after query), voice (response skin), response_type (e.g.  LLM models), and language (e.g. en-us only supported for now) here in the file. Note that the options listed here are currently the only options provided in the repository, but they are easy-to-extend as a framework later in the `helpers.py` file.

## browser compatibility
Currently, Nala works on **Chrome** and **Safari**-based browsers based on [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#javascript) standards. If you load Nala on any other browser, it will give an error message like this.

![](https://github.com/jim-schwoebel/bark_assistant/blob/main/static/images/error.png)

Note that you can find a current list of browsers that support the Web Speech API [here](https://caniuse.com/?search=Web%20Speech%20API) or in the figure below.

![](https://github.com/jim-schwoebel/bark_assistant/blob/main/static/images/wspeeech_api.png?raw=true)

## maintainers
![](https://static.wixstatic.com/media/55f531_a204ce54c8484c4294297f1252de3752~mv2.png/v1/fill/w_160,h_160,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/Erd%C5%91sLogoNewSmall.png)

This project was incubated as a result of the [Erdos Fellowship program](https://www.erdosinstitute.org/become-a-member) - and since has resulted in a larger independent initiative.

Here is a list of active maintainers to this project:

- [Jim](https://github.com/jim-schwoebel) - chief maintainer, Erdos Institute mentor
- [Jin](https://github.com/jxu81) - Erdos Institute fellow
- [Nathan](https://github.com/Finer-Things) -  Erdos Institute fellow
- [Collin](https://github.com/cjoverbay) - Data scientist @ Indeed.com (project advisor)

If you'd like to help maintain this project, reach out to Jim Schwoebel @ jim@schwoebel.me and he can invite you to our weekly call to ship PRs and delegate work in our sprint cycle.

## references 
Here is a quick list of references for additional reading. 

### javascript front-end 
- [audio.js](http://kolber.github.io/audiojs/) - playback audio alternative (setting)
- [bootstrap icons](https://icons.getbootstrap.com/) - use bootstrap and bootstrap icons for javascript front-end
- [howlers.js](https://github.com/goldfire/howler.js) - playback audio for assistant
- [recorder.js](https://github.com/mattdiamond/Recorderjs) - to record audio files with bootstrap icon buttons
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#javascript)
- [wavesurfer.js](https://wavesurfer-js.org/) - for enumerating last audio file generated in the browser
### feature extraction
- [python_speech_features](https://github.com/jim-schwoebel/allie/blob/master/features/audio_features/pspeech_features.py) - audio feature extraction method useed
### ML models (used)
- [Dolly-v2-3b](https://huggingface.co/databricks/dolly-v2-3b) - LLM (Databricks) 
- [SpeechT5 model](https://huggingface.co/microsoft/speecht5_tts) - text-to-speech synthesis (Microsoft)
- [Whisper API](https://huggingface.co/docs/transformers/model_doc/whisper) - speech-to-text (SOTA)
- [RLHF](https://medium.com/aiguys/reinforcement-learning-from-human-feedback-instructgpt-and-chatgpt-693d00cb9c58) - human feedback.
### future tools used
- [auth0](https://github.com/auth0) - authentication / tokens
- [minio](https://github.com/minio/minio) - minio is an object storage platform
