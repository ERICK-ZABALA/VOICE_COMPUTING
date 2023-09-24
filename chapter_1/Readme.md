# VOICE COMPUTING

# Chapter 1 - Voice Computing Fundamentals

Fundamentals:

+ Mic selection - sound in electrical signal amps C/s
+ Saving and Manipulating Audio Files
+ Audio Codecs
+ Compress Audio

--- mic -> sound card (Audio data IN / OUT) --- SEND ANALOG FORMAT (amps C/s) OR DIGITAL FORMAT (linear PCM data) --- > through buses.
--- playback -> speakers or headphones --- sound card change DIGITAL FORMAT to ANALOG FORMAT
--- convert digital stream an audio codec is a software program used to encode and decode (pcm data -- wav -- pcm data).
--- an audio coding format is output file type of signal digital to .wav
--- audio transcoding convert to different audio coding format. wav to mp3

--- audio channel -- reperesent number audio in and out to record audio signal.--- stereo and mono.

In short, to play mono or stereo audio, you need a speaker. Speakers convert electrical signals into sound and can be customized with multiple drivers to enhance audio quality by dividing frequencies into tweeters 2000 20000 Hz (highs), midrange drivers (mids) 250 - 2000 Hz, and woofers (lows) 40 - 500 Hz. Mono audio plays the same on all speakers, while stereo uses independent channels for a more immersive experience. Optionally, subwoofers are drivers added separately from the loudspeaker enclosure to reproduce ultra low frequencies <200 Hz.

# Read Write Audio

Read and write Audio Files

# Library PyDub

+ Install: sudo apt-get install ffmpeg
+ pip install pydub

```python
from pydub import AudioSegment
# read/write data convert format
data = AudioSegment.from_wav("audio/one.wav")
data.export("audio/new_one.wav")
```

+ sample rate = (samples/sec)
+ raw data samples = (numeric value frames) --- reflect power amplitude of the signal

# Manipulating Audio Files

+ install sudo apt-get install sox libsox-dev
+ pip install sox

```python
import os
# change channel audio one.wav to stereo.wav
os.system('sox audio/one.wav -c 2 audio/stereo.wav')
# combine two audios and the output file is three.wav
os.system('sox audio/stereo.wav audio/two.wav audio/three.wav')
# increase volumen
os.system('sox -v 4.0 audio/three.wav audio/volup.wav')
# trim = cut specific part of the audio 3 sec
os.system('sox audio/volup.wav audio/trim.wav trim 0 3')
# reverse
os.system('sox audio/volup.wav audio/reverse.wav reverse')

```

# Playing Audio

Synchronous playback: Audio plays within Python code and blocks other code.
Asynchronous playback: Allows executing background code while audio plays.

# Synchronous

pip install pygame

```python
import pygame

def sync_playback(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

sync_playback('audio/one.wav')

```

# Asynchronous

sudo apt install libpulse0
sudo apt-get install pulseaudio
sudo apt-get install alsa-utils -y
sudo pulseaudio --start -v
W: [pulseaudio] main.c: This program is not intended to be run as root (unless --system is specified).
I: [pulseaudio] main.c: Daemon startup successful.
aplay -l
aplay: device_list:277: no soundcards found...

then doing his steps in Windows 10:

https://x410.dev/cookbook/wsl/enabling-sound-in-wsl-ubuntu-let-it-sing/

![Alt text](images\image.png)

![Alt text](images\image-1.png)

pip install sounddevice

```python
import sounddevice as sd
import soundfile as sf
import time

def async_playback(filename):
    data, fs = sf.read(filename)
    sd.play(data, fs)
    return data, fs

data, fs = async_playback('audio/one.wav')
# can execute commands
print('Able to execute this before finishing')
print('Hi, this is cool!')
# can stop after 1 second playing back
time.sleep(1)
sd.stop()
print('stopped')
```
# Record Async

```python
import sounddevice as sd
import soundfile as sf
import time

def printstuff(number):
    for i in range(number):
        print(i)

def async_record(filename, duration, fs, channels):
    print('recording')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    print('can to execute this before finishing')
    printstuff(30)

    sd.wait()
    sf.write(filename, myrecording, fs)
    print('done recording')

async_record('async_record.wav', 10, 16000, 1)

```
# Converting Audio Formats

+ Install ffmpeg in Windows Variable Path before

![Alt text](images\image-9.png)

```pytthon
import ffmpy

def convert_wav(filename):
    #take in an audio file and convert with ffpeg file type
    #types of input files: .mp3
    #output file type: .wav
    if filename[-4:] in ['.mp3','.m4a','.ogg']:
        ff = ffmpy.FFmpeg(
            inputs={filename:None},
            outputs={filename[0:-4]+'.wav': None}
            )
        ff.run()

convert_wav('audio/one.mp3')

```
![Alt text](images\image-2.png)

# Transcript Speech to Text

+ Connect to Speech-to-Text API by Google

![Alt text](images\image-3.png)

![Alt text](images\image-4.png)

![Alt text](images\image-5.png)

+ Console Google - Project STT Google

![Alt text](images\image-6.png)

```bash
$ gcloud auth application-default login
previous paste code: pass: 4...
devnet_code@cloudshell:~ (stt-voice-400016)$ cat /tmp/tmp.Gf7JLDNgHI/application_default_credentials.json
```

+ Copy application_default_credentials.json in your local machine.

```bash
$ export GOOGLE_APPLICATION_CREDENTIALS='/d/DEVOPS/VOICE_COMPUTING/VOICE_COMPUTING/chapter_1/04_transcript_audio/application_default_credentials.json'
$ echo $GOOGLE_APPLICATION_CREDENTIALS
```

```python

import speech_recognition as sr_audio
import sounddevice as sd
import soundfile as sf
import os, json, datetime

def transcribe_audio_google(filename):
    # transcribe the audio (note this is only done if a voice sample)
    r=sr_audio.Recognizer()
    with sr_audio.AudioFile(filename) as source:
        audio = r.record(source)
    text=r.recognize_google_cloud(audio_data=audio, language="es-BO")

    return text

def sync_record(filename, duration, fs, channels):
    print('recording')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, fs)
    print('done recording')

def store_transcript(filename, transcript):
    jsonfilename=filename[0:-4]+'.json'
    print('saving %s to current directory'%(jsonfilename))
    data = {
        'date': str(datetime.datetime.now()),
        'filename':filename,
        'transcript':transcript,
        }
    print(data)
    jsonfile=open(jsonfilename,'w')
    json.dump(data,jsonfile)
    jsonfile.close()

# record file and print transcript
filename='google_record.wav'
sync_record(filename, 10, 16000, 1)
transcript=transcribe_audio_google(filename)
# now write the transcript into a .json file
# e.g. google_record.wav transcript will be stored in google_record.json
store_transcript(filename, transcript)
```
![Alt text](images\image-7.png)

+ https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages

![Alt text](images\image-11.png)

# Text to Speech TTS

+ Enable in Google Text to Speech
+ Use credentials: GOOGLE_APPLICATION_CREDENTIALS

![Alt text](images\image-8.png)

+ https://cloud.google.com/text-to-speech/docs/voices

```python
def speak_google(text, filename, model):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code='fr-CA',
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        name=model
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(filename, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file %s' % (filename))

# Experimenta con varias voces
base = 'output'
models = [
    'fr-CA-Neural2-A',
    'fr-CA-Neural2-B',
    'fr-CA-Neural2-C',
    ]

text = 'Hola, Montreal Google TTS'

# Recorre varias voces y genera archivos de audio
# Todos estos archivos se guardarán en el directorio actual
for model in models:
    speak_google(text, f'{base}_{model}.mp3', model)

```
![Alt text](images\image-10.png)

# Upload File OneDrive

+ Active Google Drive API

![Alt text](images\image-13.png)

![Alt text](images\image-14.png)

+ Create an Account for your Application

![Alt text](images\image-12.png)

![Alt text](images\image-15.png)

+ Store file as client_secrets.json
```python
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Autenticación con Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Abre una ventana del navegador para autenticar

# Crea una conexión a Google Drive
drive = GoogleDrive(gauth)

# Ruta local del archivo de audio
local_file_path = 'audio/one.mp3'

try:
    # Nombre que quieres darle al archivo en Google Drive
    drive_file_name = 'google_tts.mp3'
    # Sube el archivo al directorio raíz de Google Drive
    file = drive.CreateFile({'title': drive_file_name})
    # Establece el contenido del archivo desde la ubicación local
    file.SetContentFile(local_file_path)
    file.Upload()
    # Verifica si la carga se realizó correctamente
    if file.uploaded:
        print('Archivo de audio subido a Google Drive con éxito.')
    else:
        print('No se pudo cargar el archivo correctamente.')

except Exception as e:
    print('Se produjo un error en: ', e)

```
![Alt text](images\image-16.png)