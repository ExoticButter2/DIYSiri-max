import serial
import openwakeword
import os
import HelperModules.Prompting.PromptFunctions as PromptFunctions
import HelperModules.WakeWord.WakeWordFunctions as WakeWordFunctions
import settings

state = 0#0 for wake word, 1 for prompt

base_directory = os.path.dirname(os.path.abspath(__file__))
onnx_model_path = os.path.join(base_directory, "mahcks.onnx")

model = openwakeword.Model(wakeword_models = [onnx_model_path], inference_framework = "onnx")
 
def HeaderProcess(headers):#check if headers are valid depending on mode
    if state == 0:
        if headers[0] == 0xAA and headers[1] == 0x55:#wake word sampling start
            WakeWordFunctions.WakeWordProcessStart()
    else:
        if headers[0] == 0x0 and headers[1] == 0xFF:#prompt sampling start
            PromptFunctions.PromptSampleStart()
        elif headers[0] == 0xF0 and headers[1] == 0x0F:#prompt sampling end
            PromptFunctions.PromptSampleEnd()
    return False  

while True:
    headers = settings.serialComm.read(2)
    
    if headers:
        HeaderProcess(headers)
        