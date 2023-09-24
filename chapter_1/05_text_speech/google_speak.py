def speak_google(text, filename, model):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
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
    'en-US-Wavenet-A',
    'en-US-Wavenet-B',
    'en-US-Wavenet-C',
    'en-US-Wavenet-D',
    'en-US-Wavenet-E',
    'en-US-Wavenet-F'
]

text = 'Hey, I am testing out Google TTS'

# Recorre varias voces y genera archivos de audio
# Todos estos archivos se guardarán en el directorio actual
for model in models:
    speak_google(text, f'{base}_{model}.mp3', model)
