import os
import openwakeword
import serial

global base_directory
global onnx_model_path
global state
global model
global serialComm
    
base_directory = os.path.dirname(os.path.abspath(__file__))
onnx_model_path = os.path.join(base_directory, "mahcks.onnx")
state = 0#0 for wake word, 1 for prompt
model = openwakeword.Model(wakeword_models = [onnx_model_path], inference_framework = "onnx")
serialComm = serial.Serial("/dev/serial0", 500000, timeout = 1)