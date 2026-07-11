import wave
import numpy
import os

workspacePath = os.getcwd()

def WriteWaveFile(fileName, sampleRate, audioData:numpy.ndarray):
    path = os.path.join(workspacePath, fileName)
    
    if os.path.exists(path):#remove previous prompts
        os.remove(path)
    
    with wave.open(path, 'wb') as waveFile:
        waveFile.setnchannels(1)
        waveFile.setsampwidth(2)
        waveFile.setframerate(sampleRate)
        
        waveFile.writeframes(audioData.tobytes())
        print(f"Wave file {fileName} written!")
        
    return path