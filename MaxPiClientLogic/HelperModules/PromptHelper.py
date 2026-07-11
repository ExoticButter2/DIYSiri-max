from google import genai
from HelperModules import WaveFileWriter
import edge_tts
import os

client = genai.Client()

workspacePath = os.getcwd()
audioResponsePath = os.path.join(workspacePath, "promptResponse.wav")

def ProcessPrompt(dataArray):#returns text response from audio
    print("Processing prompt")
    promptPath = WaveFileWriter.WriteWaveFile("prompt.wav", 16000)#writes file and returns path
    
    audioFile = client.files.upload(file=promptPath)
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite", contents=["Write a 50 word response to this audio clip:", audioFile]
    )
    
    print("Processed prompt")
    return response.text

def ConvertPromptTextToAudio(textResponse):
    if os.path.exists(audioResponsePath):
        os.remove(audioResponsePath)
    
    communicate = edge_tts.Communicate(text=textResponse, voice="en-US-BrianNeural")
    communicate.save_sync(audioResponsePath)
    
    return audioResponsePath