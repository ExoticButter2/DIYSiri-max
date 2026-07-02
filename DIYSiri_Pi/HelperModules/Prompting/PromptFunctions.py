import HelperModules.HelperForHelper.WaveFileWriting as WaveFileWriting
import os
import settings
import HelperModules.AIPromptToText.AIPrompting as AIPromptHelper

def SendPrompt():
    print("Sending prompt")#WORK ON
    promptDirectory = os.path.join(settings.base_directory, "prompt.wav")
    #with open(promptDirectory, 'rb') as waveFile:
    
def ProcessPrompt(prompt):
    print("Processing prompt")
    parsed_samples = []
    
    for i in range(0, len(prompt), 2):
        sample = prompt[i:i+2]
        convertedSample = (int.from_bytes(sample, byteorder = 'little', signed = False) - 256) << 7
        
        parsed_samples.append(convertedSample)
        
    WaveFileWriting.WriteWaveFile("prompt.wav", parsed_samples)#AFTER THAT PLAY SOUND FROM PROMPT RESPONSE AND RESET STATE (WIP)
    textResponse = AIPromptHelper.AudioPromptToText(settings.base_directory + "/prompt.wav")
    
    if textResponse:
        print("Text response generated")
        #process text response through local tts model and play audio
        
        
def PromptSampleStart():
    print("Started sampling for prompt")
    
def PromptSampleEnd():
    print("Finished sampling for prompt")
    data = settings.serialComm.read_all()
    ProcessPrompt(data)