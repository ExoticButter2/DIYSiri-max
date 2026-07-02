import HelperModules.HelperForHelper.WaveFileWriting as WaveFileWriter
import settings
import HelperModules.AIPromptToText.AIPrompting as AIPromptHelper
import AIPromptToAudio.PromptToAudioHelper as PromptToAudio
        
def ProcessPrompt(prompt):
    print("Processing prompt")
    parsed_samples = []
    #TURNS PROMPT AUDIO INTO PROCESSABLE FORMAT
    for i in range(0, len(prompt), 2):
        sample = prompt[i:i+2]
        convertedSample = (int.from_bytes(sample, byteorder = 'little', signed = False) - 256) << 7
        
        parsed_samples.append(convertedSample)
        
    WaveFileWriter.WriteWaveFile("prompt.wav", parsed_samples, 16000)#WRITE AS WAVE FILE
    textResponse = AIPromptHelper.AudioPromptToText(settings.base_directory + "/prompt.wav")#SEND AUDIO PROMPT TO AI FOR TEXT
    
    
    if textResponse:
        print("Text response generated")
        audioResponse = PromptToAudio.GenerateWaveFileFromTextPrompt(textResponse, "response.wav")#USE AI TEXT RESPONSE FOR AUDIO TTS
        #!!!PLAY AUDIO RESPONSE TO SPEAKERS!!!
        settings.state = 0#set back to wake word mode
        
        
def PromptSampleStart():
    print("Started sampling for prompt")
    
def PromptSampleEnd():
    print("Finished sampling for prompt")
    data = settings.serialComm.read_all()
    ProcessPrompt(data)