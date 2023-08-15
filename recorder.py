# Import necessary libraries
import speech_recognition as sr
import openai
from io import BytesIO
openai_key="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" # Set the OpenAI API key

# Initialize the SpeechRecognition recognizer and microphone
r =sr.Recognizer()
mic=sr.Microphone()

# Define the Speech-to-text (STT) function for speech recognition and transcription
def STT():
    print("Listening")
    with mic as source:
        # Record audio from the microphone for a duration of 7 seconds
        audio=r.listen(source)
        # Convert the recorded audio to BytesIO object
        wav_data = BytesIO(audio.get_wav_data())
        wav_data.name = "microphone_aduio.wav"
        print("transcribing.....")
        # Use the OpenAI whisper API to transcribe the audio
        transcript = openai.Audio.transcribe("whisper-1", wav_data, api_key=openai_key,language="en")
        print(transcript["text"])
        # Append the transcribed text to a transcript file
        f = open(r"D:\Thesis\transcriptions_transcript_1.txt", "a")
        f.write(transcript["text"])
        f.close()
