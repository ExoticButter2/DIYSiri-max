from Settings import settings
import wave
import pyaudio

def PlayAudio(audioPath):#has to be .wav
    print("Playing audio")
    settings.playingAudio = True
    settings.playedAudioBefore = True
    
    waveFile = wave.open(audioPath, "rb")
    
    print(f"Channels: {waveFile.getnchannels()}")
    print(f"Sample rate: {waveFile.getframerate()}")
    print(f"Format: {settings.pyAudioInstance.get_format_from_width(waveFile.getsampwidth())}")
    
    speakerStream = settings.pyAudioInstance.open(format=pyaudio.get_format_from_width(waveFile.getsampwidth()), 
                                                  output=True, 
                                                  channels=waveFile.getnchannels(),
                                                  rate = waveFile.getframerate())
    
    data = waveFile.readframes(waveFile.getnframes())
    
    speakerStream.write(data)
    
    speakerStream.stop_stream()
    speakerStream.close()
    settings.playingAudio = False
    print("Finished playing audio")