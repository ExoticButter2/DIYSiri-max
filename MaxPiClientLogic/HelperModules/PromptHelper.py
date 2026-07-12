from google import genai
from HelperModules import WaveFileWriter
import edge_tts
import subprocess
import time
import os

client = genai.Client()
scriptFolderDir = os.getcwd()

def ProcessPrompt(dataArray):#returns text response from audio
    print("Processing prompt")
    promptPath = WaveFileWriter.WriteWaveFile("prompt.wav", 16000, dataArray)#writes file and returns path
    
    audioFile = client.files.upload(file=promptPath)
    
    while audioFile.state.name == "PROCESSING":
        print("Processing...")
        time.sleep(2)
        audioFile = genai.get_file(audioFile.name)
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite", contents=["Do not transcribe the audio file. Instead analyze the spoken sentence and provide an answer to the sentence:", audioFile]
    )
    
    client.files.delete(name=audioFile.name)
    
    print("Processed prompt")
    return response.text

def ConvertPromptTextToAudio(textResponse):
    wav_filePath = os.path.join(scriptFolderDir, "promptResponse.wav")
    mp_filePath = os.path.join(scriptFolderDir, "promptResponse.mp3")

    if os.path.exists(mp_filePath):
        os.remove(mp_filePath)

    communicate = edge_tts.Communicate(text=textResponse, voice="ar-LY-OmarNeural")
    communicate.save_sync(mp_filePath)

    subprocess.run(['ffmpeg', '-y', '-i', mp_filePath, '-ar', '48000', '-ac', '2', '-f', 'wav', wav_filePath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    os.remove(mp_filePath)

    return wav_filePath