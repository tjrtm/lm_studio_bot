import pyttsx3
import os
import numpy as np
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
from openai import OpenAI

engine = pyttsx3.init()

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    speak("Yo Bro, what's up! ")
    #print("Hi there, what's up! Tell me how may I help you.")

def takecommand():
    model_path = "vosk"  # Adjust the model path as needed
    if not os.path.exists(model_path):
        print("Model path is incorrect or the model is not found. Please modify the model_path variable.")
        return None

    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)

    try:
        with sd.RawInputStream(samplerate=16000, channels=1, dtype='int16') as stream:
            print("Listening...")
            while True:
                data, overflowed = stream.read(4096)
                if overflowed:
                    print("Overflow! Please speak a bit quieter.")
                    continue
                data_bytes = np.frombuffer(data, dtype='int16').tobytes()
                if rec.AcceptWaveform(data_bytes):
                    result = json.loads(rec.Result())['text']
                    print("Recognizing...")
                    print(result)
                    return result.lower()
                else:
                    rec.PartialResult()
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def send_and_speak(message):
    response = client.chat.completions.create(
        model="mradermacher/DevsDoCode-LLama-3-8b-Uncensored-GGUF", # change with your model from LM-studio
        messages=[
            {"role": "system", "content": "You're a Bro and best buddy, be polite and friendly with your answers"},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
    )
    server_response = response.choices[0].message.content  # Corrected line
    print("Server responded:", server_response)
    speak(server_response)

if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand()
        if query:
            send_and_speak(query)
