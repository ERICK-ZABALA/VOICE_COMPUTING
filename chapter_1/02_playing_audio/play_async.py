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
