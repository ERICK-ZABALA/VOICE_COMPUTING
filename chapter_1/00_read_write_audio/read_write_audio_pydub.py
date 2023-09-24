from pydub import AudioSegment
# read/write data
# sample rate = (samples/sec)
data = AudioSegment.from_wav("audio/one.wav")

data.export("audio/new_one_pydub.wav")