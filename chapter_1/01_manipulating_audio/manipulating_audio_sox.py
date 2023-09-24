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
