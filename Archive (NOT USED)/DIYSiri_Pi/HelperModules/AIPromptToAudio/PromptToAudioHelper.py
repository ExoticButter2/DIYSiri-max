from kittentts import KittenTTS
import HelperForHelper.WaveFileWriting as WaveFileWriter
import settings

model = KittenTTS("KittenML/kitten-tts-nano-0.8-int8")

def GenerateWaveFileFromTextPrompt(prompt, fileName):
    filePath = settings.base_directory + "/" + fileName
    
    audio = model.generate(prompt, voice = 'Leo')
    responseAudioFile = WaveFileWriter.WriteWaveFile(filePath, audio, 24000)
    
    if not responseAudioFile:
        print("Error when generating audio response file")
        return None
    
    return responseAudioFile