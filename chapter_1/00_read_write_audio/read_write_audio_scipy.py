from scipy.io import wavfile
fs, data = wavfile.read('audio/one.wav')
wavfile.write('audio/new_one_scipy.wav', fs, data)
