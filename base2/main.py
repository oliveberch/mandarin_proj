import speech_recognition as sr
from langdetect import detect
from transformers import pipeline
from gtts import gTTS
import os
import time

# Initialize speech recognizer and translation pipeline
recognizer = sr.Recognizer()
translator = pipeline('translation_zh_to_en', model='Helsinki-NLP/opus-mt-zh-en')

# Function to capture audio from microphone
def capture_audio():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        return audio

# Function to recognize speech
def recognize_speech(audio):
    try:
        text = recognizer.recognize_google(audio, language='zh-CN')
        print(f"Recognized text: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

# Function to detect language
def detect_language(text):
    return detect(text)

# Function to translate text
def translate_text(text):
    translation = translator(text)
    return translation[0]['translation_text']

# Function to convert text to speech
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    filename = f"output_{int(time.time())}.mp3"
    tts.save(filename)
    os.system(f"start {filename}")

# Main function to process audio
def process_audio():
    audio = capture_audio()
    if audio:
        text = recognize_speech(audio)
        if text:
            detected_lang = detect_language(text)
            if detected_lang == 'zh-cn':
                translated_text = translate_text(text)
                print(f"Translated text: {translated_text}")
                text_to_speech(translated_text)

process_audio()
