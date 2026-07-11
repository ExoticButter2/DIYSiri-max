from Settings import settings
from HelperModules import PyAudioHelper
import wave

def PlayAudio(audioPath):#has to be .wav
    print("Playing audio")
    settings.playingAudio = True
    settings.playedAudioBefore = True
    
    waveFile = wave.open(audioPath, "rb")
    
    speakerStream = settings.pyAudioInstance.open(format=settings.pyAudioInstance.get_format_from_width(waveFile.getsampwidth()), 
                                                  output=True, 
                                                  output_device_index=PyAudioHelper.FindWMDeviceIndex('output'),
                                                  channels=waveFile.getnchannels(),
                                                  rate = waveFile.getframerate())
    
    data = waveFile.readframes(waveFile.getnframes())
    
    speakerStream.write(data)
    
    speakerStream.stop_stream()
    speakerStream.close()
    settings.playingAudio = False
    print("Finished playing audio")