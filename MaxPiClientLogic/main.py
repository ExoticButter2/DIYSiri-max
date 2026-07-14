from HelperModules import AudioRecording
from HelperModules import AudioPlaying
from HelperModules import Networking
from Settings import settings
import socket
import os
import struct
import soundfile as sf
import numpy

SERVER_WAKE_WORD_HEADER = 0
SERVER_PROMPT_HEADER = 1
CLIENT_PROMPT_HEADER = 2
CLIENT_PROMPT_RESPONSE_HEADER = 3
SERVER_ERROR_HEADER = 4

PC_IP = "192.168.178.162"
PORT = 4000

audioFolderPath = os.path.dirname(os.path.abspath(__file__))
audioResponsePath = os.path.join(audioFolderPath, "promptResponse.wav")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((PC_IP, PORT))

client_socket.setblocking(True)

processingPrompt = False

settings.state = 0#0 for wake word, 1 for prompt
lastState = 0

while True:
    print(settings.state)
    if settings.state == 0:#if wake word mode
        if lastState == 1:#if previously prompted
            AudioRecording.ClearStreamBuffer()
        
        lastState = 0
        audioBuffer = AudioRecording.GetWMRecordingBuffer()
        rms, db = AudioRecording.GetBufferLoudness(audioBuffer)
        
        print(f"Loudness: {db}")
        
        try:
            if rms != 0:
                networkDataHeader = struct.pack('!BI', SERVER_WAKE_WORD_HEADER, audioBuffer.nbytes)#send wake word
                client_socket.sendall(networkDataHeader)
                client_socket.sendall(audioBuffer)
            else:
                continue
        except BlockingIOError:
            pass
        
        
        receiveHeader = Networking.ReceiveStrict(5, client_socket)
            
        header, size = struct.unpack('!BI', receiveHeader)
        
        if header != CLIENT_PROMPT_HEADER:
            print("Wrong header!")
            continue
            
        response = Networking.ReceiveStrict(size, client_socket)
        decodedResponse = response.decode("utf-8")
        
        print(f"Received: {decodedResponse}")
                
        if decodedResponse == "TRIGGERED":
            AudioRecording.ClearStreamBuffer()
            settings.state = 1
            print("Wake word found")
                    
            AudioPlaying.PlayAudio(os.path.join(os.getcwd(), "maxwhat.wav"))
            settings.playedAudioBefore = False
        elif decodedResponse == "UNTRIGGERED":
            print("No wake word found")
    elif settings.state == 1:#if prompt mode
        if not settings.playingAudio and settings.playedAudioBefore:#check if audio just finished playing
            settings.playedAudioBefore = False
            settings.state = 0#set back to wake word mode after audio playing
            continue
        elif settings.playingAudio:
            continue
        
        if not processingPrompt:
            processingPrompt = True
            promptArray = AudioRecording.RecordPrompt()
            promptNetworkDataHeader = struct.pack('!BI', SERVER_PROMPT_HEADER, promptArray.nbytes)
            client_socket.sendall(promptNetworkDataHeader)
            client_socket.sendall(promptArray)
        
        if promptArray.size == 0:
            print("Prompt array is empty!")
            continue
        
        byteArray = Networking.ReceiveStrict(5, client_socket)
        
        print(f"Received prompt response header: {byteArray}")
        header, size = struct.unpack('!BI', byteArray)
        
        if header == SERVER_ERROR_HEADER:
            print("Server error!")
            processingPrompt = False
            continue
        
        if header != CLIENT_PROMPT_RESPONSE_HEADER:
            print("Not client prompt response header!")
            continue
        
        processingPrompt = False
        promptResponseArray = Networking.ReceiveStrict(size, client_socket)#returns a 24khz audio array
        
        convertedResponseArray = numpy.frombuffer(promptResponseArray, dtype=numpy.float32)
        sf.write("promptResponse.wav", convertedResponseArray, 24000)
        print("Received prompt response audio")
        
        if not os.path.exists(audioResponsePath):
            print("No prompt response audio path found")
            continue
        
        
        AudioPlaying.PlayAudio(audioResponsePath)
        lastState = 1