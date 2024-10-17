import pyaudio
import numpy as np
import speech_recognition as sr
from langdetect import detect
from transformers import pipeline
from gtts import gTTS
import io
from pydub import AudioSegment
from pydub.playback import play



# Parameters for audio
CHUNK = 4096  # Larger buffer size to capture more meaningful chunks of speech
FORMAT = pyaudio.paInt16  # 16-bit format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (44.1kHz)

# Initialize PyAudio and speech recognizer
p = pyaudio.PyAudio()
recognizer = sr.Recognizer()
translator = pipeline('translation_zh_to_en', model='Helsinki-NLP/opus-mt-zh-en')

# Function to recognize speech from chunks
def recognize_speech_from_audio(audio_data):
    try:
        text = recognizer.recognize_google(audio_data, language='zh-CN')
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

# Function to convert text to speech and play it directly through speakers
def text_to_speech_direct(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts_fp = io.BytesIO()
    tts.save(tts_fp)
    tts_fp.seek(0)

    # Load the TTS data into an audio segment
    audio_segment = AudioSegment.from_file(tts_fp, format="mp3")

    # Play the audio segment directly through the speakers
    play(audio_segment)

# Real-time audio stream processing
def process_audio_stream():
    # Open stream for input (microphone)
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print("Listening for speech in real-time... Press Ctrl+C to stop.")
    audio_frames = []

    try:
        while True:
            # Read audio chunk from input stream
            audio_chunk = stream.read(CHUNK)
            audio_frames.append(audio_chunk)

            # Convert byte data to audio data for speech recognition
            audio_data = b''.join(audio_frames)
            audio_wav = sr.AudioData(audio_data, RATE, 2)

            # Perform speech recognition once enough data is captured
            if len(audio_frames) > 20:  # Adjust this threshold for timing
                print("Processing captured audio...")
                text = recognize_speech_from_audio(audio_wav)

                if text:
                    detected_lang = detect_language(text)
                    if detected_lang == 'zh-cn':
                        translated_text = translate_text(text)
                        print(f"Translated text: {translated_text}")
                        text_to_speech_direct(translated_text)

                # Clear frames after processing to listen for new sentences
                audio_frames = []

    except KeyboardInterrupt:
        print("\nProcessing stopped.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Audio stream closed.")

# Run the continuous audio processing
process_audio_stream()