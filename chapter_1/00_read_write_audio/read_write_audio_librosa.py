import librosa
import soundfile as sf

y, sr = librosa.load('audio/one.wav')
sf.write('audio/new_one_librosa.wav', y, sr)
