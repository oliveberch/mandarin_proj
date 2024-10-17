## this is for a sample operation to 2x the volume


import pyaudio
import numpy as np

CHUNK = 1024  # Buffer size
FORMAT = pyaudio.paInt16  # 16-bit format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (44.1kHz)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Define the audio operation function (example: volume adjustment)
def operation(audio_chunk):
    # Convert bytes data to numpy array
    audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
    
    # Example operation: increase volume by a factor of 2
    processed_audio = audio_data * 2

    # Ensure the values are within the valid range for 16-bit audio (-32768 to 32767)
    processed_audio = np.clip(processed_audio, -32768, 32767)
    
    # Convert numpy array back to bytes
    return processed_audio.astype(np.int16).tobytes()

# Open stream for input (microphone) and output (speakers)
stream_in = p.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK)

stream_out = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

print("Processing audio in real-time...")

try:
    while True:
        # Read audio chunk from the input stream
        input_data = stream_in.read(CHUNK)

        # Process the audio chunk using the operation function
        output_data = operation(input_data)

        # Write the processed chunk to the output stream (speakers)
        stream_out.write(output_data)

except KeyboardInterrupt:
    print("\nProcessing stopped.")

# Stop and close the streams
stream_in.stop_stream()
stream_in.close()
stream_out.stop_stream()
stream_out.close()
p.terminate()

print("Streams closed.")
