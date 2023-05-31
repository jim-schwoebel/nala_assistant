# nala_assistant

Nala is an exceptional voice assistant framework specifically designed to cater to developers' needs. With its user-friendly architecture and straightforward extensibility, Nala empowers developers to create customized voice assistants effortlessly. Seamlessly integrate voice capabilities into your applications and devices, and provide users with a truly interactive and hands-free experience.

![](https://media.giphy.com/media/VDzVG8lvNRufu/giphy.gif)

Key Features for Developers:

- **Extensible Architecture:** Nala offers a flexible and modular architecture that allows developers to extend its functionality with ease. Integrate voice commands, natural language processing, and intelligent responses into your projects effortlessly.
- **Customized Voice Actions:** Define and customize voice commands to suit your application's requirements. Empower users to interact with your software using natural language, enhancing the overall user experience.
- **Rapid Integration:** With Nala's intuitive APIs and comprehensive documentation, integrating voice capabilities into your projects is a breeze. Save development time and effort while providing a powerful voice interface for your users.
- **Multi-Platform Support:** Nala is designed to work seamlessly across various platforms and operating systems. Whether you're building web applications, mobile apps, or even IoT devices, Nala can be easily integrated into your technology stack.
- **Machine Learning Capabilities:** Leverage Nala's built-in machine learning capabilities to improve voice recognition accuracy and enhance the overall intelligence of your voice assistant. Train and fine-tune the model to adapt to specific user requirements.
- **Privacy and Security:** Nala prioritizes user privacy and data security. Rest assured that all voice interactions are handled with utmost care, ensuring the confidentiality and integrity of user information.

Note that this is a web-enabled version of [a prior voice assistant app here](https://github.com/jim-schwoebel/nala).

## getting started
Install basic dependencies:
```
sudo apt-get install ffmpeg
git clone git@github.com:jim-schwoebel/bark_assistant.git
cd bark_assistant
virtualenv env 
source env/bin/activate
pip3 install -r requirements.txt
```
Generate a secret key for `SESSION_SECRET`, `JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY` and environment vars using the following line of code 3 times (save this in `.env`)
```
python -c 'import secrets; print(secrets.token_hex())'
```
To open and edit .env file
```
nano .env
```
Then run the app:
```
uvicorn app:app --reload
```

You will now be able to visit localhost (`http://127.0.0.1:8000`) to use appication.

## deploying to server
1. get a cloudflare account.
2. setup app on a cloud provider 
3. deploy using the instructions below

## javascript front-endd 
- [bootstrap icons](https://icons.getbootstrap.com/) - use bootstrap and bootstrap icons for javascript front-end
- [recorder.js](https://github.com/mattdiamond/Recorderjs) - to record audio files with bootstrap icon buttons
- [howlers.js](https://github.com/goldfire/howler.js) - playback audio for assistant
- [wavesurfer.js](https://wavesurfer-js.org/) - for enumerating last audio file generated in the browser
- [audio.js](http://kolber.github.io/audiojs/) - playback audio alternative (setting)

## feature extraction
- [python_speech_features](https://github.com/jim-schwoebel/allie/blob/master/features/audio_features/pspeech_features.py) - audio feature extraction method useed
- [audio_features - Allie](https://github.com/jim-schwoebel/allie/tree/master/features/audio_features)

## browser compatibility
Currently, Nala works on Chrome and Safari-based browsers based on [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#javascript) standards. If you load Nala on any other browser, it will give an error message like this.

![](https://github.com/jim-schwoebel/bark_assistant/blob/main/static/images/error.png)

## future tools used
- [minio](https://github.com/minio/minio) - minio is an object storage platform
- [auth0](https://github.com/auth0) - authentication
