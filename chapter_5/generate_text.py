from tensorflow.python.keras.utils.multi_gpu_utils import multi_gpu_model

from textgenrnn import textgenrnn

textgen = textgenrnn.TextgenRnn(is_gpu=False)

try:
    textgen.train_from_file('textmessages.txt', num_epochs=1)
except Exception as e:
    print(f"Error during training: {e}")

newmsgs = list()
for i in range(10):
    try:
        newmsg = textgen.generate()
        newmsgs.append(newmsg)
    except Exception as e:
        print(f"Error during text generation: {e}")
