import openwakeword
import serial
import os

serialComm = serialComm = serial.Serial("/dev/serial0", 500000, timeout = 1)

base_directory = os.path.dirname(os.path.abspath(__file__))
onnx_model_path = os.path.join(base_directory, "mahcks.onnx")

model = openwakeword.Model(wakeword_models = [onnx_model_path], inference_framework = "onnx")

def ProcessSample(sampleArray):#array of 1280 16-bit signed ints
    global state
    
    print("Processing sample..")
    scores = model.predict(sampleArray)
    
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
        sampleArray.append(sample)#add 16 bit signed int to array
    
    if len(sampleArray) == 1280:#make sure to be right length
        ProcessSample(sampleArray)