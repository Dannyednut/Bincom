import warnings
import torch
import numpy as np
import speech_recognition as sr

from typing import Generator
from queue import Queue
from time import sleep
from threading import Event
from faster_whisper import WhisperModel

# Constants
VOLUME_THRESHOLD = 500
ENERGY_THRESHOLD = 3000
RECORD_TIMEOUT = 5
MODEL_NAME = "small.en"
VAD_THRESHOLD = 0.5
MIN_SILENCE_MS = 300
SAMPLE_RATE = 16000
FILTER_PHRASES = {"thank you"}

warnings.filterwarnings("ignore")


def is_audio_loud_enough(audio_data: bytes, volume_threshold: int = VOLUME_THRESHOLD) -> bool:
    """Check if audio volume exceeds a defined threshold."""
    audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
    volume = np.sqrt(np.mean(np.square(audio_array)))
    return volume > volume_threshold


def select_microphone() -> int:
    """Prompt user to select a microphone device."""
    print("Available microphone devices:")
    mic_list = sr.Microphone.list_microphone_names()
    for index, name in enumerate(mic_list):
        print(f"{index}: {name}")
    return int(input("Select a microphone by index: "))


def transcribe_audio(mic_index: int, listening_event: Event) -> Generator[str, None, None]:
    """
    Transcribes audio from the microphone using faster-whisper with VAD.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = ENERGY_THRESHOLD
    recognizer.dynamic_energy_threshold = True

    model = WhisperModel(MODEL_NAME, device=device, compute_type=compute_type)
    data_queue: Queue[bytes] = Queue()

    source = sr.Microphone(sample_rate=SAMPLE_RATE, device_index=mic_index)
    with source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    def record_callback(recognizer: sr.Recognizer, audio: sr.AudioData) -> None:
        """Push loud enough audio to the queue."""
        if listening_event.is_set():
            data = audio.get_raw_data()
            if is_audio_loud_enough(data):
                data_queue.put(data)
                return True
        else:
            return False

    stop_listening = recognizer.listen_in_background(
        source, record_callback, phrase_time_limit=RECORD_TIMEOUT
    )
    sleep(10)
    print("🎤 Listening... Press Ctrl+C to stop.")

    try:
        while True:
            if not data_queue.empty():
                # Combine queued audio
                audio_data = b''.join(list(data_queue.queue))
                data_queue.queue.clear()

                # Convert to float32 and normalize
                audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
                max_val = np.max(np.abs(audio_array))
                if max_val > 0:
                    audio_array /= max_val

                segments, _ = model.transcribe(
                    audio_array,
                    vad_filter=True,
                    vad_parameters={
                        "threshold": VAD_THRESHOLD,
                        "min_silence_duration_ms": MIN_SILENCE_MS,
                    },
                    language="en",
                )
               
                for segment in segments:
                    text = segment.text.strip()

                    if (
                        segment.no_speech_prob < 0.4
                        and text
                        and text.lower() not in FILTER_PHRASES
                    ):
                        listening_event.clear()
                        if not record_callback(sr.Recognizer, sr.AudioData):
                            yield text

            sleep(0.01)

    except KeyboardInterrupt:
        print("\n🛑 Transcription service stopped.")
        stop_listening()
