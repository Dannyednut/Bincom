import threading
from voice import select_microphone, transcribe_audio
from response import generate_response, tts


def main() -> None:
    is_listening = threading.Event()
    is_listening.set()  # Start in listening mode

    mic_index: int = select_microphone()
    for text in transcribe_audio(mic_index, is_listening):
        if text:
            is_listening.clear()
            response: str = generate_response(text)
            tts(response)
            is_listening.set()


if __name__ == "__main__":
    main()
