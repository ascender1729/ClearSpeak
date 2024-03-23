import os
import queue
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import pyaudio
from google.cloud import speech

# Set the Google Cloud service account key file for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'E:/ClearSpeak_Keys/clearspeak-418017-8c3c58665bdc.json'

# Audio recording parameters optimized for speech recognition
RATE = 16000  # Sample rate is 16000 Hz, suitable for speech recognition
CHUNK = int(RATE / 10)  # Buffer size (100ms), optimal for real-time responsiveness
stop_transcription = False  # Global flag to control the transcription

class MicrophoneStream:
    """Manages the microphone stream, yielding audio chunks for processing."""

    def __init__(self, rate, chunk):
        self.rate = rate
        self.chunk = chunk
        self.buffer = queue.Queue()
        self.closed = True

    def __enter__(self):
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self.rate,
            input=True, frames_per_buffer=self.chunk,
            stream_callback=self.fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.closed = True
        self.buffer.put(None)
        self.audio_interface.terminate()

    def fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collects data from the audio stream into a buffer."""
        self.buffer.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Yields audio chunks from the buffer."""
        while not self.closed:
            chunk = self.buffer.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self.buffer.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

def listen_print_loop(responses, text_widget, stop_flag):
    """Processes and prints transcriptions from the Speech-to-Text API."""
    for response in responses:
        if stop_flag():
            break
        if not response.results or not response.results[0].alternatives:
            continue

        result = response.results[0]
        transcript = result.alternatives[0].transcript

        if result.is_final:
            text_widget.insert(tk.END, transcript + '\n')
            text_widget.see(tk.END)

def start_transcription(text_widget, stop_flag):
    """Starts the transcription process."""
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='en-US',
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)
        responses = client.streaming_recognize(streaming_config, requests)
        listen_print_loop(responses, text_widget, stop_flag)

def main():
    """Main function to run the Tkinter GUI application."""
    def stop_transcription_callback():
        """Callback function to stop the transcription process."""
        global stop_transcription
        stop_transcription = True

    def start_transcription_callback():
        """Callback function to start the transcription process."""
        global stop_transcription
        stop_transcription = False
        threading.Thread(target=start_transcription, args=(text_widget, lambda: stop_transcription), daemon=True).start()

    root = tk.Tk()
    root.title("Real-Time Transcription")

    text_widget = ScrolledText(root, wrap=tk.WORD)
    text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    start_button = tk.Button(root, text="Start Transcription", command=start_transcription_callback)
    start_button.pack(side=tk.LEFT, padx=10, pady=10)

    stop_button = tk.Button(root, text="Stop Transcription", command=stop_transcription_callback)
    stop_button.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()
