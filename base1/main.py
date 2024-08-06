import pyaudio
import speech_recognition as sr
from googletrans import Translator

# func to get continous microphone stream
def get_microphone_stream():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    return audio, stream

# func to recognize mandarin 
def recognize_speech(audio_data):
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio_data, language='zh-CN')
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

# func to translate Mandarin
def translate_text(text, src='zh-CN', dest='en'):
    translator = Translator()
    translation = translator.translate(text, src=src, dest=dest)
    return translation.text


audio, stream = get_microphone_stream()
recognizer = sr.Recognizer()
translator = Translator()

try:
    while True:
        with sr.Microphone(sample_rate=44100, chunk_size=1024) as source:
            print("Listening...")
            audio_data = recognizer.listen(source, timeout=5)
            mandarin_text = recognize_speech(audio_data)
            
            if mandarin_text:
                print("Detected Mandarin: ", mandarin_text)
                english_translation = translate_text(mandarin_text)
                print("Translation: ", english_translation)

except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()

