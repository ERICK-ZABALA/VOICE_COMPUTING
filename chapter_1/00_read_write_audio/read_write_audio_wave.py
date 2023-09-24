import wave
# read/write data
# sample rate = (samples/sec)
data = wave.open('audio/one.wav', mode='rb')
params=data.getparams() 
print("params:", params)
#params: _wave_params(nchannels=1, sampwidth=2, framerate=16000, nframes=47104, comptype='NONE', compname='not compressed')
