from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import sounddevice as sd
import subprocess
import queue
import json
import sys
import os


load_dotenv() 
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
api_key = os.getenv("OPENAI_API_KEY")

def get_response(user_message):
    system_prompt = "You are an evil robot and you want to eliminate the human race. you give short responses and are quite aggresive. you are exstitential" # weird prompt i know but it's for a video so give me a break

    response = client.chat.completions.create(model = "gpt-4-turbo",  messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}], temperature = 1) 

    reply = response.choices[0].message.content
    print(reply)

    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d_%H-%M-%S.") + f"{now.microsecond // 1000:03d}"
    filename = f"reply_{formatted_time}.mp3"

    response = client.audio.speech.create(model="tts-1", voice="onyx", input=reply)

    with open(filename, "wb") as f:
        f.write(response.content)

    subprocess.run(["afplay", filename])

    # os.remove("reply.mp3")

q = queue.Queue()

# Audio callback to fill queue
def callback(indata, frames, time, status):
    if status:
        print(status, file = sys.stderr)
    q.put(bytes(indata))

# Load model
model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

# Open audio stream from mic
with sd.RawInputStream(samplerate = 16000, blocksize = 8000, dtype = 'int16', channels = 1, callback = callback):
    print("Speak into the microphone:")
    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print("Recognized:", result['text'])
            get_response(result['text'])
        else:
            partial = json.loads(recognizer.PartialResult())
            print("Partial:", partial['partial'])