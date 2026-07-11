import openwakeword
import os
import socket
import numpy

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDRESS = ("0.0.0.0", 4000)

server_socket.bind(ADDRESS)
server_socket.listen(1)

print("Waiting for pi..")
connection, address = server_socket.accept()
print(f"Connected to {address}")

threshold = 0.5

mainFolderPath = os.path.dirname(os.path.abspath(__file__))
modelPath = os.path.join(mainFolderPath, "mahcks.onnx")

model = openwakeword.Model(wakeword_models=[modelPath], inference_framework="onnx")

audioBufferArray = bytearray()
FRAME_SIZE = 2560

def AnalyzeAudioBuffer(buffer):
    result = model.predict(buffer)
    
    for mdl in result.keys():
        print(f"Result score: {result[mdl]}")
        if result[mdl] >= threshold:
            model.reset()
            print("Wake word found!")
            return True
        
    return False

while True:
    try:
        data = connection.recv(4096)
        print("Received data")
        if not data:
            break
        
        audioBufferArray.extend(data)
    except BlockingIOError:
        pass
    
    while len(audioBufferArray) >= FRAME_SIZE:
            frame_data = audioBufferArray[:FRAME_SIZE]#save frame
            del audioBufferArray[:FRAME_SIZE]#clear frame
            numpyData = numpy.frombuffer(frame_data, dtype=numpy.int16)
            
            if AnalyzeAudioBuffer(numpyData):
                connection.send(b"TRIGGERED\n")
                print("Wake word detected")