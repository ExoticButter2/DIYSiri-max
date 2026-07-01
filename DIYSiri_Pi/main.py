import serial
import openwakeword
import os
import wave
import struct

state = 0#0 for wake word, 1 for prompt
serialComm = serial.Serial("/dev/serial0", 500000, timeout = 1)

base_directory = os.path.dirname(os.path.abspath(__file__))
onnx_model_path = os.path.join(base_directory, "mahcks.onnx")

model = openwakeword.Model(wakeword_models = [onnx_model_path], inference_framework = "onnx")

def SendPrompt():
    print("Sending prompt")#WORK ON
    promptDirectory = os.path.join(base_directory, "prompt.wav")
    #with open(promptDirectory, 'rb') as waveFile:

def WriteWaveFile(filename, data):
    bytesData = struct.pack(f"{len(data)}h", *data)
    
    with wave.open(filename, 'wb') as waveFile:
        waveFile.setchannels(1)
        waveFile.setsampwidth(2)
        waveFile.setframerate(16000)
        waveFile.writeframes(bytesData)

def ProcessSample(sample):
    global state
    
    print("Processing sample..")
    scores = model.predict(sample)
    
    if scores["mahcks"] > 0.5:
        print("Wake word detected")
        serialComm.write(b'\x01')#send prompt mode start signal
        state = 1#set to prompt mode
        serialComm.reset_input_buffer()

def WakeWordProcessStart():
    conversionData = serialComm.read(2560)
    
    sampleArray = []
    
    for i in range(0, len(conversionData), 2):
        rawSample = int.from_bytes(conversionData[i:i+2], byteorder = 'little', signed = False)#unsigned 9 bit
        sample = (rawSample - 256) << 7#signed 16 bit
        sampleArray.append(sample)
    
    if len(sampleArray) == 1280:#make sure to be right length
        ProcessSample(sampleArray)
        
def ProcessPrompt(prompt):
    print("Processing prompt")
    parsed_samples = []
    
    for i in range(0, len(prompt), 2):
        sample = prompt[i:i+2]
        convertedSample = (int.from_bytes(sample, byteorder = 'little', signed = False) - 256) << 7
        
        parsed_samples.append(convertedSample)
        
    WriteWaveFile("prompt.wav", parsed_samples)#AFTER THAT PLAY SOUND FROM PROMPT RESPONSE AND RESET STATE (WIP)
        
        
def PromptSampleStart():
    print("Started sampling for prompt")
    
def PromptSampleEnd():
    print("Finished sampling for prompt")
    data = serialComm.read_all()
    ProcessPrompt(data)
 
        
def HeaderProcess(headers):#check if headers are valid depending on mode
    if state == 0:
        if headers[0] == 0xAA and headers[1] == 0x55:#wake word sampling start
            WakeWordProcessStart()
    else:
        if headers[0] == 0x0 and headers[1] == 0xFF:#prompt sampling start
            PromptSampleStart()
        elif headers[0] == 0xF0 and headers[1] == 0x0F:#prompt sampling end
            PromptSampleEnd()
    return False  

while True:
    headers = serialComm.read(2)
    
    if headers:
        HeaderProcess(headers)
        