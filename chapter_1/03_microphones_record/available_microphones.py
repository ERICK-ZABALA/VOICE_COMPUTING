import sounddevice as sd

mics = sd.query_devices()
default_devices = sd.default.device
default_input = default_devices[0]
default_output = default_devices[1]
# prints all available devices
for i in range(len(mics)):
    print(mics[i])
# can set default device easily with
sd.default.device = 0
