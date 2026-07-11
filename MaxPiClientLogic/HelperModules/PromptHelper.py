from google import genai
from HelperModules import WaveFileWriter
import edge_tts
import subprocess

client = genai.Client()

scriptFolderDir = os.path.dirname(os.path.abspath(__file__))

def ProcessPrompt(dataArray):#returns text response from audio
    print("Processing prompt")
    promptPath = WaveFileWriter.WriteWaveFile("prompt.wav", 16000, dataArray)#writes file and returns path
    
    audioFile = client.files.upload(file=promptPath)
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite", contents=["Write a 50 word response to this audio clip:", audioFile]
    )
    
    print("Processed prompt")
    return response.text

def ConvertPromptTextToAudio(textResponse):
    wav_filePath = os.path.join(scriptFolderDir, "promptResponse.wav")
    mp_filePath = os.path.join(scriptFolderDir, "promptResponse.mp3")
    
    if os.path.exists(mp_filePath):
        os.remove(mp_filePath)
    
    communicate = edge_tts.Communicate(text=textResponse, voice="en-US-BrianNeural")
    communicate.save_sync(mp_filePath)
    
    subprocess.run(['ffmpeg', '-y', '-i', mp_filePath, wav_filePath])
        
    #subprocess.call(['ffmpeg', '-i', mpFilePath, os.path.join(scriptFolderDir, "promptResponse.wav")])
    os.remove(mp_filePath)
    
    return os.path.join(scriptFolderDir, "promptResponse.wav")