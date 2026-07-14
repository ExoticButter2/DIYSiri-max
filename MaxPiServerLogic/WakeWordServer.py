import openwakeword
import os
import socket
import numpy
from HelperModules import Prompting
from HelperModules import Networking
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDRESS = ("0.0.0.0", 4000)

server_socket.bind(ADDRESS)
server_socket.listen(1)
server_socket.settimeout(30)

print("Waiting for pi..")
connection, address = server_socket.accept()
print(f"Connected to {address}")

threshold = 0.5

mainFolderPath = os.path.dirname(os.path.abspath(__file__))
modelPath = os.path.join(mainFolderPath, "mahcks.onnx")

model = openwakeword.Model(wakeword_model_paths=[modelPath])

utfTRIGGERED = "TRIGGERED".encode("utf-8")
utfUNTRIGGERED = "UNTRIGGERED".encode("utf-8")
utfTRIGGEREDSize = len("TRIGGERED".encode("utf-8"))
utfUNTRIGGEREDSize = len("UNTRIGGERED".encode("utf-8"))

audioBufferArray = bytearray()
FRAME_SIZE = 2560

SERVER_WAKE_WORD_HEADER = 0
SERVER_PROMPT_HEADER = 1
CLIENT_PROMPT_HEADER = 2
CLIENT_PROMPT_RESPONSE_HEADER = 3
SERVER_ERROR_HEADER = 4

def AnalyzeAudioBuffer(buffer):
    convertedAudioBuffer = numpy.frombuffer(buffer, dtype=numpy.int16)
    result = model.predict(convertedAudioBuffer)
    
    for mdl in result.keys():
        print(f"Result score: {result[mdl]}")
        if result[mdl] >= threshold:
            model.reset()
            print("Wake word found!")
            return True

    return False

def SendErrorToClient():
    errorStruct = struct.pack('!BI', SERVER_ERROR_HEADER, 0)
    connection.sendall(errorStruct)

while True:
    print("Waiting for pi header..")
    headerByteArray = Networking.ReceiveStrict(5, connection)
    
    header, size = struct.unpack('!BI', headerByteArray)
    dataByteArray = Networking.ReceiveStrict(size, connection)
    
    numpyDataArray = numpy.frombuffer(dataByteArray, dtype=numpy.int16)
    
    if header == SERVER_WAKE_WORD_HEADER:
        if AnalyzeAudioBuffer(dataByteArray):
            connection.sendall(struct.pack('!BI', CLIENT_PROMPT_HEADER, utfTRIGGEREDSize))
            connection.sendall(utfTRIGGERED)
            print("Wake word detected")
        else:
            connection.sendall(struct.pack('!BI', CLIENT_PROMPT_HEADER, utfUNTRIGGEREDSize))
            connection.sendall(utfUNTRIGGERED)
    elif header == SERVER_PROMPT_HEADER:
        print("Prompt data!")
        print("Processing audio prompt..")
        textPrompt = Prompting.ProcessAudioPrompt(numpyDataArray)
        
        if not textPrompt:
            SendErrorToClient()
            print("No text prompt generated!")
            continue
        
        print("Processing text prompt..")
        textResponse = Prompting.ProcessTextPrompt(textPrompt)
        
        if not textResponse:
            SendErrorToClient()
            print("No text response generated!")
            continue
        
        print("Converting text response to audio..")
        audioResponseArray = Prompting.ConvertTextResponseToAudio(textResponse)
        
        if audioResponseArray.size == 0:
            SendErrorToClient()
            print("No audio response generated!")
            continue
        
        print("Conversion finished!")
        promptResponseNetworkHeader = struct.pack('!BI', CLIENT_PROMPT_RESPONSE_HEADER, audioResponseArray.nbytes)
        
        connection.sendall(promptResponseNetworkHeader)
        connection.sendall(audioResponseArray)