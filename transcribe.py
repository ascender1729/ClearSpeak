import os
import queue
import threading
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import pyaudio
from google.cloud import speech

# Set the Google Cloud service account key file for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'E:/ClearSpeak_Keys/clearspeak-418017-8c3c58665bdc.json'

# Audio recording parameters optimized for speech recognition
RATE = 16000
CHUNK = int(RATE / 10)
stop_transcription = False

class MicrophoneStream:
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
        self.buffer.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
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
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='en-US',
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
        responses = client.streaming_recognize(streaming_config, requests)
        listen_print_loop(responses, text_widget, stop_flag)

def main():
    def stop_transcription_callback():
        global stop_transcription
        stop_transcription = True

    def start_transcription_callback():
        global stop_transcription
        stop_transcription = False
        threading.Thread(target=start_transcription, args=(text_widget, lambda: stop_transcription), daemon=True).start()

    root = tk.Tk()
    root.title("Clear Speak")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    text_widget = ScrolledText(root, wrap=tk.WORD)
    text_widget.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    start_button = ttk.Button(root, text="Start Transcription", command=start_transcription_callback)
    start_button.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
    stop_button = ttk.Button(root, text="Stop Transcription", command=stop_transcription_callback)
    stop_button.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

    # Make the buttons equal width and responsive
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    # Adjust the main window's minimum size
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    main()

