from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from pydub import AudioSegment
from response import generate_response, tts
import os
import urllib.parse

app = FastAPI()
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.get("/webhooks/answer")
async def answer_call():
    ncco = [
        {
            "action": "talk",
            "text": "Hello, this is your AI assistant. How can I help you today?"
        },
        {
            "action": "record",
            "eventUrl": ["https://your-server.com/webhooks/recording"],
            "endOnSilence": 3,
            "beepStart": True
        }
    ]
    return JSONResponse(content=ncco)

@app.post("/webhooks/recording")
async def process_recording(request: Request):
    data = await request.json()
    recording_url = data.get("recording_url")
    
    if not recording_url:
        return JSONResponse(content={"error": "No recording URL received."}, status_code=400)

    # Download audio
    filename = os.path.join(AUDIO_DIR, "user_input.wav")
    os.system(f"curl -s {urllib.parse.quote(recording_url, safe=':/')} -o {filename}")

    # Transcribe audio locally (you can use whisper or your faster_whisper)
    from faster_whisper import WhisperModel
    model = WhisperModel("base.en")
    segments, _ = model.transcribe(filename)
    user_input = " ".join([seg.text for seg in segments])

    if "goodbye" in user_input.lower():
        return JSONResponse([{"action": "talk", "text": "Goodbye!"}, {"action": "hangup"}])
    # Generate response
    ai_response = generate_response(user_input)
    tts(ai_response)

    # Convert to 8000Hz mono for Vonage
    wav_path = os.path.join(AUDIO_DIR, "output.wav")
    audio = AudioSegment.from_wav(wav_path).set_frame_rate(8000).set_channels(1)
    audio.export(wav_path, format="wav")

    return JSONResponse([
        {
            "action": "stream",
            "streamUrl": ["https://your-server.com/audio/output.wav"]
        },
        {
            "action": "record",
            "eventUrl": ["https://your-server.com/webhooks/recording"],
            "endOnSilence": 3,
            "beepStart": True
        }
    ])

@app.post("/webhooks/input")
async def handle_input(request: Request):
    data = await request.json()

    # Extract speech text
    speech = data.get("speech", {})
    user_text = speech.get("text", "")

    if not user_text:
        return JSONResponse(content=[
            {"action": "talk", "text": "Sorry, I didn't catch that. Please try again."},
            {
                "action": "input",
                "type": ["speech"],
                "eventUrl": ["https://your-server.com/webhooks/input"]
            }
        ])

    if "goodbye" in user_text.lower():
        return JSONResponse(content=[
            {"action": "talk", "text": "Goodbye!"},
            {"action": "hangup"}
        ])
    # Generate AI response
    ai_response = generate_response(user_text)

    # Return response and wait for next input
    return JSONResponse(content=[
        {
            "action": "talk",
            "text": ai_response
        },
        {
            "action": "input",
            "type": ["speech"],
            "eventUrl": ["https://your-server.com/webhooks/input"]
        }
    ])

@app.get("/audio/{filename}")
async def serve_audio(filename: str):
    filepath = os.path.join(AUDIO_DIR, filename)
    return FileResponse(filepath, media_type="audio/wav")
