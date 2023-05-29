# bark_assistant
bark assistant - some thoughts on how to make the Bark model into a voice assistant.

## getting started
```
sudo apt-get install ffmpeg
git clone git@github.com:jim-schwoebel/bark_assistant.git
cd bark_assistant
virtualenv env 
source env/bin/activate
pip3 install -r requirements.txt
uvicorn app:app --reload
```

You will now be able to visit localhost (`http://127.0.0.1:8000`) to use appication.

## deploying to server
1. get a cloudflare account.
2. setup app on a cloud provider 

## tools used
- [minio](https://github.com/minio/minio) - minio is an object storage platform
- [auth0](https://github.com/auth0) - authentication

## javascript front-endd 
- [bootstrap icons](https://icons.getbootstrap.com/) - use bootstrap and bootstrap icons for javascript front-end
- [recorder.js](https://github.com/mattdiamond/Recorderjs) - to record audio files with bootstrap icon buttons
- [howlers.js](https://github.com/goldfire/howler.js) - playback audio for assistant
- [wavesurfer.js](https://wavesurfer-js.org/) - for enumerating last audio file generated in the browser
- [audio.js](http://kolber.github.io/audiojs/) - playback audio alternative (setting)

## feature extraction
- [meyda](https://github.com/meyda/meyda) - audio feature extraction and visualization

## audio annotation
- [peak.js](https://waveform.prototyping.bbc.co.uk/) - peak.js is an audio annotation library