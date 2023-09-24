import soundfile as sf
data, fs = sf.read('audio/one.wav')
sf.write('audio/new_one_soundfile.wav', data, fs)
