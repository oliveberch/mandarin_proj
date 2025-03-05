# Architecture:

1. **Microphone Input**:
   - Use the `speech_recognition` library to capture live audio from the microphone.
   - Ensure that the microphone is properly set up and tested to capture clear audio.

2. **Language Detection**:
   - Initially, you can use the `langdetect` library to detect the language. However, for more sophisticated models, consider integrating pre-trained language detection models available from libraries like `transformers`. [`torch` & `tensorflow` as required by transformers] tf-keras

3. **Translation**:
   - Use a pre-trained translation model from the `transformers` library for translating Mandarin to English.
   - Models such as `Helsinki-NLP/opus-mt-zh-en` can be fine-tuned for better performance if necessary.

4. **Audio Output**:
   - Use the `gtts` library to convert translated text to speech.
   - Ensure the output audio quality is clear and understandable.

## Observation:

- the audio input is segmented for a short duration
- the processing time to translate is high
